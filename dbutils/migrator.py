from dbutils.helpers import upsert, batch_upsert
from typing import Dict, List, Any
from collections import defaultdict


class MigratorMixIn:
    _BATCH_QUEUE: Dict[str, list] = defaultdict(list)
    _MAX_QUEUE_SIZE: int = 300
    COLUMN_MAP: Dict[str, List[str]] = {
        "collaborators": [
            "nct_id",
            "responsible_party_type",
            "investigator_name",
            "investigator_affiliation",
            "collaborator_name",
            "collaborator_class",
            "collaborator_type",
        ],
        "conditions": ["nct_id", "name"],
        "contact": ["nct_id", "name", "role", "phone", "email"],
        "design": [
            "nct_id",
            "study_type",
            "expanded_access_individual",
            "expanded_access_intermediate",
            "expanded_access_treatment",
            "patient_registry",
            "num_phases",
            "allocation",
            "intervention_model",
            "primary_purpose",
            "observational_model",
            "biospec_retention",
            "biospec_description",
            "enrollment_count",
        ],
        "eligibility": [
            "nct_id",
            "accepts_healthy_volunteers",
            "gender",
            "gender_based",
            "min_age",
            "max_age",
            "population_description",
            "sampling_method",
        ],
        "facility": [
            "nct_id",
            "name",
            "status",
            "city",
            "state",
            "zip",
            "country",
            "contacts",
        ],
        "interventions": [
            "nct_id",
            "intervention_type",
            "intervention_name",
            "intervention_description",
            "group_label",
        ],
        "officials": ["nct_id", "name", "role", "affiliation"],
        "phases": ["nct_id", "phase"],
        "oversight": [
            "nct_id",
            "oversight_has_dmc",
            "is_fda_regulated_drug",
            "is_fda_regulated_device",
            "is_ppsd",
            "is_us_export",
            "is_unapproved_device",
            "is_fda_violation",
        ],
        "outcome": ["nct_id", "type", "measure", "description", "time_frame"],
        "status": [
            "nct_id",
            "status_verified_date",
            "overall_status",
            "last_known_status",
            "why_stopped",
            "start_date",
            "primary_completion_date",
            "completion_date",
            "study_first_submit_date",
            "study_first_submit_qc_date",
            "study_first_post_date",
            "results_waived",
            "results_first_submit_date",
            "results_first_submit_qc_date",
            "results_first_post_date",
            "last_update_submit_date",
            "last_update_post_date",
        ],
        "identification": [
            "nct_id",
            "nct_id_alias",
            "num_nct_aliases",
            "org_study_id",
            "org_study_id_type",
            "org_study_id_link",
            "num_secondary_ids",
            "brief_title",
            "official_title",
            "acronym",
            "org_name",
            "org_class",
            "brief_summary",
            "detailed_description",
            "num_conditions",
        ],
        "groups": [
            "nct_id",
            "group_type",
            "group_description",
            "group_label",
        ],
    }
    CONFLICT_COLUMNS: Dict[str, List[str]] = {
        "collaborators": [
            "nct_id",
            "responsible_party_type",
            "investigator_name",
            "investigator_affiliation",
            "collaborator_name",
            "collaborator_class",
            "collaborator_type",
        ],
        "conditions": ["nct_id", "name"],
        "contact": ["nct_id", "name", "role", "phone", "email"],
        "design": ["nct_id"],
        "eligibility": ["nct_id"],
        "facility": ["nct_id", "name", "status", "city", "state", "zip", "country"],
        "groups": ["nct_id", "group_type", "group_description", "group_label"],
        "identification": ["nct_id"],
        "interventions": [
            "nct_id",
            "intervention_type",
            "intervention_name",
            "intervention_description",
            "group_label",
        ],
        "officials": ["nct_id", "name", "role", "affiliation"],
        "phases": ["nct_id", "phase"],
        "oversight": ["nct_id"],
        "outcome": ["nct_id", "type", "measure", "description", "time_frame"],
        "status": ["nct_id"],
    }

    @staticmethod
    def add_to_batch(table_name: str, data: List[Any]) -> None:
        MigratorMixIn._BATCH_QUEUE[table_name].append(data)
        if len(MigratorMixIn._BATCH_QUEUE[table_name]) >= MigratorMixIn._MAX_QUEUE_SIZE:
            MigratorMixIn._flush_batch(table_name)

    @staticmethod
    def _flush_batch(table_name: str) -> None:
        try:
            batch_upsert(
                table_name,
                MigratorMixIn.COLUMN_MAP[table_name],
                MigratorMixIn._BATCH_QUEUE[table_name],
                MigratorMixIn.CONFLICT_COLUMNS[table_name],
            )
            MigratorMixIn._BATCH_QUEUE[table_name].clear()
        except Exception as e:
            print(f"Error flushing batch for table {table_name}: {e}")
            raise e

    @staticmethod
    def flush_all_batches() -> None:
        for table_name in MigratorMixIn._BATCH_QUEUE:
            MigratorMixIn._flush_batch(table_name)

    @staticmethod
    def upsert_table(table_name: str, values: List[Any], batch: bool = False) -> None:
        if batch:
            MigratorMixIn.add_to_batch(table_name, values)
        else:
            upsert(
                table_name,
                MigratorMixIn.COLUMN_MAP[table_name],
                values,
                MigratorMixIn.CONFLICT_COLUMNS[table_name],
            )

    @staticmethod
    def migrate_collaborators(
        nct_id: str,
        responsible_party_type: str,
        investigator_name: str,
        investigator_affiliation: str,
        collaborator_name: str,
        collaborator_class: str,
        collaborator_type: str,
        batch: bool = False,
    ) -> None:
        values = [
            nct_id,
            responsible_party_type,
            investigator_name,
            investigator_affiliation,
            collaborator_name,
            collaborator_class,
            collaborator_type,
        ]
        MigratorMixIn.upsert_table("collaborators", values, batch)

    @staticmethod
    def migrate_conditions(nct_id: str, name: str, batch: bool = False) -> None:
        values = [nct_id, name]
        MigratorMixIn.upsert_table("conditions", values, batch)

    @staticmethod
    def migrate_status(
        nct_id: str,
        status_verified_date: str,
        overall_status: str,
        last_known_status: str,
        why_stopped: str,
        start_date: str,
        primary_completion_date: str,
        completion_date: str,
        study_first_submit_date: str,
        study_first_submit_qc_date: str,
        study_first_post_date: str,
        results_waived: bool,
        results_first_submit_date: str,
        results_first_submit_qc_date: str,
        results_first_post_date: str,
        last_update_submit_date: str,
        last_update_post_date: str,
        batch: bool = False,
    ) -> None:
        values = [
            nct_id,
            status_verified_date,
            overall_status,
            last_known_status,
            why_stopped,
            start_date,
            primary_completion_date,
            completion_date,
            study_first_submit_date,
            study_first_submit_qc_date,
            study_first_post_date,
            results_waived,
            results_first_submit_date,
            results_first_submit_qc_date,
            results_first_post_date,
            last_update_submit_date,
            last_update_post_date,
        ]
        MigratorMixIn.upsert_table("status", values, batch)

    @staticmethod
    def migrate_phases(nct_id: str, phase: str, batch: bool = False) -> None:
        values = [nct_id, phase]
        MigratorMixIn.upsert_table("phases", values, batch)

    @staticmethod
    def migrate_oversight(
        nct_id: str,
        oversight_has_dmc: bool,
        is_fda_regulated_drug: bool,
        is_fda_regulated_device: bool,
        is_ppsd: bool,
        is_us_export: bool,
        is_unapproved_device: bool,
        is_fda_violation: bool,
        batch: bool = False,
    ) -> None:
        values = [
            nct_id,
            oversight_has_dmc,
            is_fda_regulated_drug,
            is_fda_regulated_device,
            is_ppsd,
            is_us_export,
            is_unapproved_device,
            is_fda_violation,
        ]
        MigratorMixIn.upsert_table("oversight", values, batch)

    @staticmethod
    def migrate_outcome(
        nct_id: str,
        type: str,
        measure: str,
        description: str,
        time_frame: str,
        batch: bool = False,
    ) -> None:
        values = [nct_id, type, measure, description, time_frame]
        MigratorMixIn.upsert_table("outcome", values, batch)

    @staticmethod
    def migrate_officials(
        nct_id: str, name: str, role: str, affiliation: str, batch: bool = False
    ) -> None:
        values = [nct_id, name, role, affiliation]
        MigratorMixIn.upsert_table("officials", values, batch)

    @staticmethod
    def migrate_interventions(
        nct_id: str,
        intervention_type: str,
        intervention_name: str,
        intervention_description: str,
        group_label: str,
        batch: bool = False,
    ) -> None:
        values = [
            nct_id,
            intervention_type,
            intervention_name,
            intervention_description,
            group_label,
        ]
        MigratorMixIn.upsert_table("interventions", values, batch)

    @staticmethod
    def migrate_identification(
        nct_id: str,
        nct_id_alias: list,
        num_nct_aliases: int,
        org_study_id: str,
        org_study_id_type: str,
        org_study_id_link: str,
        num_secondary_ids: int,
        brief_title: str,
        official_title: str,
        acronym: str,
        org_name: str,
        org_class: str,
        brief_summary: str,
        detailed_description: str,
        num_conditions: int,
        batch: bool = False,
    ) -> None:
        values = [
            nct_id,
            nct_id_alias,
            num_nct_aliases,
            org_study_id,
            org_study_id_type,
            org_study_id_link,
            num_secondary_ids,
            brief_title,
            official_title,
            acronym,
            org_name,
            org_class,
            brief_summary,
            detailed_description,
            num_conditions,
        ]
        MigratorMixIn.upsert_table("identification", values, batch)

    @staticmethod
    def migrate_groups(
        nct_id: str,
        group_type: str,
        group_description: str,
        group_label: str,
        batch: bool = False,
    ) -> None:
        values = [nct_id, group_type, group_description, group_label]
        MigratorMixIn.upsert_table("groups", values, batch)

    @staticmethod
    def migrate_facility(
        nct_id: str,
        name: str,
        status: str,
        city: str,
        state: str,
        zip: str,
        country: str,
        contacts: dict,
        batch: bool = False,
    ) -> None:
        values = [nct_id, name, status, city, state, zip, country, contacts]
        MigratorMixIn.upsert_table("facility", values, batch)

    @staticmethod
    def migrate_eligibility(
        nct_id: str,
        accepts_healthy_volunteers: bool,
        gender: str,
        gender_based: bool,
        min_age: str,
        max_age: str,
        population_description: str,
        sampling_method: str,
        batch: bool = False,
    ) -> None:
        values = [
            nct_id,
            accepts_healthy_volunteers,
            gender,
            gender_based,
            min_age,
            max_age,
            population_description,
            sampling_method,
        ]

        MigratorMixIn.upsert_table("eligibility", values, batch)

    @staticmethod
    def migrate_design(
        nct_id: str,
        study_type: str,
        expanded_access_individual: bool,
        expanded_access_intermediate: bool,
        expanded_access_treatment: bool,
        patient_registry: bool,
        num_phases: int,
        allocation: str,
        intervention_model: str,
        primary_purpose: str,
        observational_model: str,
        biospec_retention: str,
        biospec_description: str,
        enrollment_count: int,
        batch: bool = False,
    ) -> None:
        values = [
            nct_id,
            study_type,
            expanded_access_individual,
            expanded_access_intermediate,
            expanded_access_treatment,
            patient_registry,
            num_phases,
            allocation,
            intervention_model,
            primary_purpose,
            observational_model,
            biospec_retention,
            biospec_description,
            enrollment_count,
        ]
        MigratorMixIn.upsert_table("design", values, batch)

    @staticmethod
    def migrate_contact(
        nct_id: str,
        name: str,
        role: str,
        phone: str,
        email: str,
        batch: bool = False,
    ) -> None:
        values = [nct_id, name, role, phone, email]
        MigratorMixIn.upsert_table("contact", values, batch)
