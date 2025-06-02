from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Dict, Any
from dbutils.migrator import MigratorMixIn
import json


class OrgStudyIdInfo(BaseModel):
    id: str
    type: Optional[str] = None


class Organization(BaseModel):
    fullName: str
    class_: Optional[str] = Field(None, alias="class")


class SecondaryIdInfo(BaseModel):
    secondaryId: str
    secondaryIdType: Optional[str] = None
    secondaryIdDomain: Optional[str] = None
    secondaryIdLink: Optional[str] = None


class IdentificationModule(BaseModel):
    nctId: str
    nctIdAlias: Optional[List[str]] = Field(default_factory=list)
    numNctAliases: Optional[int] = None
    orgStudyIdInfo: Optional[OrgStudyIdInfo] = OrgStudyIdInfo(id="")
    secondaryIdInfo: Optional[SecondaryIdInfo] = SecondaryIdInfo(secondaryId="")
    numSecondaryIds: Optional[int] = None
    organization: Organization
    briefTitle: str
    officialTitle: Optional[str] = None
    acronym: Optional[str] = None


class ExpandedAccessInfo(BaseModel):
    hasExpandedAccess: Optional[bool] = None
    individual: Optional[bool] = None
    intermediate: Optional[bool] = None
    treatment: Optional[bool] = None


class DateTypeMixin:
    @field_validator(
        "startDateType",
        "primaryCompletionDateType",
        "completionDateType",
        "studyFirstSubmitDateType",
        "studyFirstSubmitQcDateType",
        "studyFirstPostDateType",
        "lastUpdateSubmitDateType",
        "lastUpdatePostDateType",
        "resultsFirstSubmitDateType",
        "resultsFirstSubmitQcDateType",
        "resultsFirstPostDateType",
        mode="before",
        check_fields=False,
    )
    @classmethod
    def validate_date_type(cls, v):
        # Basic validation for date format (could be enhanced)
        if v not in ["ACTUAL", "ESTIMATED", "ANTICIPATED"]:
            raise ValueError("Date type must be ACTUAL, ESTIMATED, or ANTICIPATED")
        return v


class PartialDateMixin:
    @field_validator(
        "date",
        "statusVerifiedDate",
        "studyFirstSubmitDate",
        "studyFirstSubmitQcDate",
        "studyFirstPostDate",
        "lastUpdateSubmitDate",
        "lastUpdatePostDate",
        "resultsFirstSubmitDate",
        "resultsFirstSubmitQcDate",
        "resultsFirstPostDate",
        "largeDocDate",
        "largeDocUploadDate",
        mode="before",
        check_fields=False,
    )
    @classmethod
    def validate_date_format(cls, v):
        # Basic validation for date format (could be enhanced)
        if len(v.split("-")) not in [2, 3]:
            raise ValueError("Date must be in YYYY-MM or YYYY-MM-DD format")
        if len(v.split("-")) == 2:
            v += "-01"
        return v


class DateStruct(BaseModel, PartialDateMixin, DateTypeMixin):
    date: Optional[str] = None
    type: Optional[str] = None


class StatusModule(BaseModel, PartialDateMixin):
    statusVerifiedDate: Optional[str] = None
    overallStatus: Optional[str] = None
    lastKnownStatus: Optional[str] = None
    delayedPosting: Optional[bool] = None
    expandedAccessInfo: Optional[ExpandedAccessInfo] = ExpandedAccessInfo()
    startDateStruct: Optional[DateStruct] = DateStruct()
    primaryCompletionDateStruct: Optional[DateStruct] = DateStruct()
    completionDateStruct: Optional[DateStruct] = DateStruct()
    studyFirstSubmitDate: Optional[str] = None
    studyFirstSubmitQcDate: Optional[str] = None
    studyFirstPostDateStruct: Optional[DateStruct] = DateStruct()
    lastUpdateSubmitDate: Optional[str] = None
    lastUpdatePostDateStruct: Optional[DateStruct] = DateStruct()
    whyStopped: Optional[str] = None
    resultsWaived: Optional[bool] = None
    resultsFirstSubmitDate: Optional[str] = None
    resultsFirstSubmitQcDate: Optional[str] = None
    resultsFirstPostDateStruct: Optional[DateStruct] = DateStruct()


class ResponsibleParty(BaseModel):
    type: Optional[str] = None
    investigatorTitle: Optional[str] = None
    investigatorAffiliation: Optional[str] = None
    investigatorFullName: Optional[str] = None
    oldNameTitle: Optional[str] = None
    oldOrganization: Optional[str] = None


class Sponsor(BaseModel):
    name: Optional[str] = None
    class_: Optional[str] = Field(None, alias="class")


class SponsorCollaboratorsModule(BaseModel):
    responsibleParty: Optional[ResponsibleParty] = ResponsibleParty()
    leadSponsor: Optional[Sponsor] = Sponsor()
    collaborators: Optional[List[Sponsor]] = Field(default_factory=list)


class OversightModule(BaseModel):
    oversightHasDmc: Optional[bool] = None
    isFdaRegulatedDrug: Optional[bool] = None
    isFdaRegulatedDevice: Optional[bool] = None
    isUsExport: Optional[bool] = None
    fdaRegulationDrug: Optional[bool] = None
    fdaRegulationDevice: Optional[bool] = None
    isPpsd: Optional[bool] = None
    isFdaRegulated: Optional[bool] = None
    isUnapprovedDevice: Optional[bool] = None
    isFdaViolation: Optional[bool] = Field(None, alias="fdaaa801Violation")


class DescriptionModule(BaseModel):
    briefSummary: Optional[str] = None
    detailedDescription: Optional[str] = None


class ConditionsModule(BaseModel):
    conditions: Optional[List[str]] = Field(default_factory=list)
    keywords: Optional[List[str]] = Field(default_factory=list)


class MaskingInfo(BaseModel):
    masking: Optional[str] = None
    maskingDescription: Optional[str] = None
    whoMasked: Optional[List[str]] = Field(default_factory=list)


class DesignInfo(BaseModel):
    allocation: Optional[str] = None
    interventionModel: Optional[str] = None
    primaryPurpose: Optional[str] = None
    maskingInfo: Optional[MaskingInfo] = MaskingInfo()
    interventionModelDescription: Optional[str] = None
    observationalModel: Optional[str] = None
    timePerspective: Optional[str] = None


class EnrollmentInfo(BaseModel):
    count: int
    type: Optional[str] = None


class BioSpec(BaseModel):
    retention: Optional[str] = None
    description: Optional[str] = None


class DesignModule(BaseModel):
    studyType: Optional[str] = None
    phases: Optional[List[str]] = Field(default_factory=list)
    expandedAccessTypes: Optional[ExpandedAccessInfo] = ExpandedAccessInfo()
    designInfo: Optional[DesignInfo] = DesignInfo()
    enrollmentInfo: Optional[EnrollmentInfo] = EnrollmentInfo(count=0)
    bioSpec: Optional[BioSpec] = BioSpec()
    patientRegistry: Optional[bool] = None
    numPhases: Optional[int] = None
    targetDuration: Optional[str] = None


class ArmGroup(BaseModel):
    label: str
    type: Optional[str] = None
    description: Optional[str] = None
    interventionNames: Optional[List[str]] = Field(default_factory=list)
    armGroupLabel: Optional[str] = None
    armGroupType: Optional[str] = None


class Intervention(BaseModel):
    type: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    armGroupLabels: Optional[List[str]] = Field(default_factory=list)
    interventionType: Optional[str] = None
    interventionName: Optional[str] = None
    otherNames: Optional[List[str]] = Field(default_factory=list)


class ArmsInterventionsModule(BaseModel):
    armGroups: Optional[List[ArmGroup]] = Field(default_factory=list)
    interventions: Optional[List[Intervention]] = Field(default_factory=list)


class Outcome(BaseModel):
    measure: Optional[str] = None
    description: Optional[str] = None
    timeFrame: Optional[str] = None
    type: Optional[str] = None
    population: Optional[str] = None
    units: Optional[str] = None
    paramType: Optional[str] = None
    dispersionType: Optional[str] = None
    categoryList: Optional[Dict[str, List[Dict[str, str]]]] = Field(
        default_factory=dict
    )


class OutcomesModule(BaseModel):
    primaryOutcomes: Optional[List[Outcome]] = Field(default_factory=list)
    secondaryOutcomes: Optional[List[Outcome]] = Field(default_factory=list)
    otherOutcomes: Optional[List[Outcome]] = Field(default_factory=list)
    otherPreSpecifiedOutcomes: Optional[List[Outcome]] = Field(default_factory=list)


class EligibilityModule(BaseModel):
    eligibilityCriteria: Optional[str] = None
    healthyVolunteers: Optional[bool] = None
    sex: Optional[str] = None
    minimumAge: Optional[str] = None
    maximumAge: Optional[str] = None
    stdAges: Optional[List[str]] = Field(default_factory=list)
    studyPopulation: Optional[str] = None
    samplingMethod: Optional[str] = None
    genderBased: Optional[bool] = None
    genderDescription: Optional[str] = None

    @field_validator("minimumAge", "maximumAge")
    def validate_age_format(cls, v):
        if v is None:
            return v
        # Validate age format (e.g., "18 Years")
        if not v.endswith(
            (
                "Year",
                "Years",
                "Month",
                "Months",
                "Week",
                "Weeks",
                "Day",
                "Days",
                "Hour",
                "Hours",
                "Minute",
                "Minutes",
                "Second",
                "Seconds",
            )
        ):
            raise ValueError(
                "Age must end with Year, Years, Month, Months, Week, Weeks, "
                "Day, Days, Hour, Hours, Minute, Minutes, Second, or Seconds"
            )
        return v


class CentralContact(BaseModel):
    name: Optional[str] = None
    role: Optional[str] = None
    phone: Optional[str] = None
    phoneExt: Optional[str] = None
    email: Optional[str] = None


class OverallOfficial(BaseModel):
    name: Optional[str] = None
    affiliation: Optional[str] = None
    role: Optional[str] = None


class GeoPoint(BaseModel):
    lat: float
    lon: float


class Location(BaseModel):
    facility: Optional[str] = None
    status: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip: Optional[str] = None
    country: Optional[str] = None
    contacts: Optional[List[CentralContact]] = Field(default_factory=list)
    investigators: Optional[List[Dict[str, str]]] = Field(default_factory=list)


class ContactsLocationsModule(BaseModel):
    centralContacts: Optional[List[CentralContact]] = Field(default_factory=list)
    overallOfficials: Optional[List[OverallOfficial]] = Field(default_factory=list)
    locations: Optional[List[Location]] = Field(default_factory=list)


class IPDSharingStatementModule(BaseModel):
    ipdSharing: Optional[str] = None
    description: Optional[str] = None
    url: Optional[str] = None
    infoType: Optional[str] = None


class MiscInfoModule(BaseModel):
    versionHolder: Optional[str] = None
    modelPredictions: Optional[Dict[str, Any]] = Field(default_factory=dict)


class BrowseLeaf(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    asFound: Optional[str] = None
    relevance: Optional[str] = None


class BrowseBranch(BaseModel):
    abbrev: Optional[str] = None
    name: Optional[str] = None


class ConditionBrowseModule(BaseModel):
    meshes: Optional[List[Dict[str, str]]] = Field(default_factory=list)
    ancestors: Optional[List[Dict[str, str]]] = Field(default_factory=list)
    browseLeaves: Optional[List[BrowseLeaf]] = Field(default_factory=list)
    browseBranches: Optional[List[BrowseBranch]] = Field(default_factory=list)


class InterventionBrowseModule(BaseModel):
    meshes: Optional[List[Dict[str, str]]] = Field(default_factory=list)
    ancestors: Optional[List[Dict[str, str]]] = Field(default_factory=list)
    browseLeaves: Optional[List[BrowseLeaf]] = Field(default_factory=list)
    browseBranches: Optional[List[BrowseBranch]] = Field(default_factory=list)


class StudyDesignInfo(BaseModel):
    designObservationalModelList: Optional[Dict[str, List[str]]] = Field(
        default_factory=dict
    )
    timePerspectiveList: Optional[Dict[str, List[str]]] = Field(default_factory=dict)


class ProtocolSection(BaseModel):
    identificationModule: IdentificationModule
    statusModule: Optional[StatusModule] = StatusModule()
    sponsorCollaboratorsModule: Optional[SponsorCollaboratorsModule] = (
        SponsorCollaboratorsModule()
    )
    oversightModule: Optional[OversightModule] = OversightModule()
    descriptionModule: Optional[DescriptionModule] = DescriptionModule()
    conditionsModule: Optional[ConditionsModule] = ConditionsModule()
    designModule: Optional[DesignModule] = DesignModule()
    armsInterventionsModule: Optional[ArmsInterventionsModule] = (
        ArmsInterventionsModule()
    )
    outcomesModule: Optional[OutcomesModule] = OutcomesModule()
    eligibilityModule: Optional[EligibilityModule] = EligibilityModule()
    contactsLocationsModule: Optional[ContactsLocationsModule] = (
        ContactsLocationsModule()
    )
    ipdSharingStatementModule: Optional[IPDSharingStatementModule] = (
        IPDSharingStatementModule()
    )
    referencesModule: Optional[Dict[str, Any]] = None


class LargeDoc(BaseModel):
    largeDocTypeAbbrev: Optional[str] = None
    largeDocHasProtocol: Optional[bool] = None
    largeDocHasSAP: Optional[bool] = None
    largeDocHasICF: Optional[bool] = None
    largeDocLabel: Optional[str] = None
    largeDocDate: Optional[str] = None  # need validation here
    largeDocUploadDate: Optional[str] = None
    largeDocFilename: Optional[str] = None
    largeDocSize: Optional[int] = None


class LargeDocumentModule(BaseModel):
    largeDocNoSAP: Optional[bool] = None
    largeDoc: Optional[LargeDoc] = None
    numLargeDocs: Optional[int] = None


class DocumentSection(BaseModel):
    largeDocumentModule: Optional[LargeDocumentModule] = LargeDocumentModule()


class DerivedSection(BaseModel):
    miscInfoModule: Optional[MiscInfoModule] = MiscInfoModule()
    conditionBrowseModule: Optional[ConditionBrowseModule] = ConditionBrowseModule()
    interventionBrowseModule: Optional[InterventionBrowseModule] = (
        InterventionBrowseModule()
    )
    studyDesignInfo: Optional[StudyDesignInfo] = StudyDesignInfo()
    hasResults: Optional[bool] = None


class ClinicalTrialStudy(BaseModel, MigratorMixIn):
    protocolSection: ProtocolSection
    derivedSection: DerivedSection
    resultsSection: Optional[Dict[str, Any]] = None

    @field_validator("protocolSection")
    def validate_protocol_section(cls, v):
        # Could add custom validation logic here
        return v

    def migrate_to_db(self, batch: bool = False, flush_all: bool = False):
        # Extract NCT ID from the identification module
        nct_id = self.protocolSection.identificationModule.nctId

        # Migrate identification data
        id_module = self.protocolSection.identificationModule
        self.migrate_identification(
            nct_id=nct_id,
            nct_id_alias=id_module.nctIdAlias,
            num_nct_aliases=id_module.numNctAliases,
            org_study_id=id_module.orgStudyIdInfo.id,
            org_study_id_type=id_module.orgStudyIdInfo.type,
            org_study_id_link=id_module.secondaryIdInfo.secondaryIdLink,
            num_secondary_ids=id_module.numSecondaryIds,
            brief_title=id_module.briefTitle,
            official_title=id_module.officialTitle,
            acronym=id_module.acronym,
            org_name=id_module.organization.fullName,
            org_class=id_module.organization.class_,
            brief_summary=self.protocolSection.descriptionModule.briefSummary,
            detailed_description=self.protocolSection.descriptionModule.detailedDescription,
            num_conditions=len(self.protocolSection.conditionsModule.conditions),
            # batch=batch,
        )

        # Migrate status data
        status_module = self.protocolSection.statusModule
        self.migrate_status(
            nct_id=nct_id,
            status_verified_date=status_module.statusVerifiedDate,
            overall_status=status_module.overallStatus,
            last_known_status=status_module.lastKnownStatus,
            why_stopped=status_module.whyStopped,
            start_date=status_module.startDateStruct.date,
            primary_completion_date=status_module.primaryCompletionDateStruct.date,
            completion_date=status_module.completionDateStruct.date,
            study_first_submit_date=status_module.studyFirstSubmitDate,
            study_first_submit_qc_date=status_module.studyFirstSubmitQcDate,
            study_first_post_date=status_module.studyFirstPostDateStruct.date,
            results_waived=status_module.resultsWaived,
            results_first_submit_date=status_module.resultsFirstSubmitDate,
            results_first_submit_qc_date=status_module.resultsFirstSubmitQcDate,
            results_first_post_date=status_module.resultsFirstPostDateStruct.date,
            last_update_submit_date=status_module.lastUpdateSubmitDate,
            last_update_post_date=status_module.lastUpdatePostDateStruct.date,
            batch=batch,
        )

        # Migrate oversight data
        oversight_module = self.protocolSection.oversightModule
        self.migrate_oversight(
            nct_id=nct_id,
            oversight_has_dmc=oversight_module.oversightHasDmc,
            is_fda_regulated_drug=oversight_module.isFdaRegulatedDrug,
            is_fda_regulated_device=oversight_module.isFdaRegulatedDevice,
            is_ppsd=oversight_module.isPpsd,
            is_us_export=oversight_module.isUsExport,
            is_unapproved_device=oversight_module.isUnapprovedDevice,
            is_fda_violation=oversight_module.isFdaViolation,
            batch=batch,
        )

        # Migrate design data
        design_module = self.protocolSection.designModule
        self.migrate_design(
            nct_id=nct_id,
            study_type=design_module.studyType,
            patient_registry=(
                design_module.studyType == "PATIENT_REGISTRY"
                if design_module.studyType
                else None
            ),
            allocation=design_module.designInfo.allocation,
            intervention_model=design_module.designInfo.interventionModel,
            primary_purpose=design_module.designInfo.primaryPurpose,
            observational_model=design_module.designInfo.observationalModel,
            enrollment_count=design_module.enrollmentInfo.count,
            expanded_access_individual=design_module.expandedAccessTypes.individual,
            expanded_access_intermediate=design_module.expandedAccessTypes.intermediate,
            expanded_access_treatment=design_module.expandedAccessTypes.treatment,
            num_phases=design_module.numPhases,
            biospec_retention=design_module.bioSpec.retention,
            biospec_description=design_module.bioSpec.description,
            batch=batch,
        )

        # Migrate phases data
        if design_module.phases:
            for phase in design_module.phases:
                self.migrate_phases(nct_id=nct_id, phase=phase)

        # Migrate eligibility data
        eligibility_module = self.protocolSection.eligibilityModule
        self.migrate_eligibility(
            nct_id=nct_id,
            accepts_healthy_volunteers=eligibility_module.healthyVolunteers,
            gender=eligibility_module.sex,
            min_age=eligibility_module.minimumAge,
            max_age=eligibility_module.maximumAge,
            gender_based=eligibility_module.genderBased,
            population_description=eligibility_module.studyPopulation,
            sampling_method=eligibility_module.samplingMethod,
            batch=batch,
        )

        # Migrate conditions data
        for condition in self.protocolSection.conditionsModule.conditions:
            self.migrate_conditions(nct_id=nct_id, name=condition, batch=batch)

        # Migrate collaborators data
        sponsor_module = self.protocolSection.sponsorCollaboratorsModule

        # Lead sponsor
        self.migrate_collaborators(
            nct_id=nct_id,
            responsible_party_type=sponsor_module.responsibleParty.type,
            investigator_name=sponsor_module.responsibleParty.investigatorFullName,
            investigator_affiliation=sponsor_module.responsibleParty.investigatorAffiliation,
            collaborator_name=sponsor_module.leadSponsor.name,
            collaborator_class=sponsor_module.leadSponsor.class_,
            collaborator_type="lead sponsor",
            batch=batch,
        )

        # Other collaborators
        for collaborator in sponsor_module.collaborators:
            self.migrate_collaborators(
                nct_id=nct_id,
                responsible_party_type=sponsor_module.responsibleParty.type,
                investigator_name=sponsor_module.responsibleParty.investigatorFullName,
                investigator_affiliation=sponsor_module.responsibleParty.investigatorAffiliation,
                collaborator_name=collaborator.name,
                collaborator_class=collaborator.class_,
                collaborator_type="collaborator",
                batch=batch,
            )

        # Migrate outcomes data
        outcomes_module = self.protocolSection.outcomesModule

        # Primary outcomes
        for outcome in outcomes_module.primaryOutcomes:
            self.migrate_outcome(
                nct_id=nct_id,
                type="primary",
                measure=outcome.measure,
                description=outcome.description,
                time_frame=outcome.timeFrame,
                batch=batch,
            )

        # Secondary outcomes
        for outcome in outcomes_module.secondaryOutcomes:
            self.migrate_outcome(
                nct_id=nct_id,
                type="secondary",
                measure=outcome.measure,
                description=outcome.description,
                time_frame=outcome.timeFrame,
                batch=batch,
            )

        # Other outcomes
        for outcome in outcomes_module.otherOutcomes:
            self.migrate_outcome(
                nct_id=nct_id,
                type="other",
                measure=outcome.measure,
                description=outcome.description,
                time_frame=outcome.timeFrame,
                batch=batch,
            )

        # Migrate interventions data
        for intervention in self.protocolSection.armsInterventionsModule.interventions:
            self.migrate_interventions(
                nct_id=nct_id,
                intervention_type=intervention.type,
                intervention_name=intervention.name,
                intervention_description=intervention.description,
                group_label=(
                    intervention.armGroupLabels[0]
                    if intervention.armGroupLabels
                    else None
                ),
                batch=batch,
            )

        # Migrate groups data
        for group in self.protocolSection.armsInterventionsModule.armGroups:
            self.migrate_groups(
                nct_id=nct_id,
                group_type=group.type,
                group_description=group.description,
                group_label=group.label,
                batch=batch,
            )

        # Migrate facility data
        for location in self.protocolSection.contactsLocationsModule.locations:
            self.migrate_facility(
                nct_id=nct_id,
                name=location.facility,
                status=location.status,
                city=location.city,
                state=location.state,
                zip=location.zip,
                country=location.country,
                contacts=(
                    json.dumps(
                        {
                            "contacts": [
                                contact.model_dump() for contact in location.contacts
                            ]
                        }
                    )
                    if location.contacts
                    else None
                ),
                batch=batch,
            )

        # Migrate contact data
        for contact in self.protocolSection.contactsLocationsModule.centralContacts:
            self.migrate_contact(
                nct_id=nct_id,
                name=contact.name,
                role=contact.role,
                phone=contact.phone,
                email=contact.email,
                batch=batch,
            )

        # Migrate official data
        for official in self.protocolSection.contactsLocationsModule.overallOfficials:
            self.migrate_officials(
                nct_id=nct_id,
                name=official.name,
                role=official.role,
                affiliation=official.affiliation,
                batch=batch,
            )

        if batch and flush_all:
            MigratorMixIn.flush_all_batches()
