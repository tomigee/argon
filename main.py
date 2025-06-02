import json
from models import ClinicalTrialStudy
from dbutils.helpers import init_database
from tqdm import tqdm


def main(init_db: bool = True):
    if init_db:
        init_database()

    with open("ctg-studies.json", "r") as f:
        clinical_studies = json.load(f)

    for i in tqdm(range(len(clinical_studies)), desc="Processing studies"):
        try:
            parsed_study = ClinicalTrialStudy.model_validate(clinical_studies[i])
            if i == len(clinical_studies) - 1:
                parsed_study.migrate_to_db(batch=True, flush_all=True)
            else:
                parsed_study.migrate_to_db(batch=True)
        except Exception as e:
            open("errors.json", "a").write(json.dumps(clinical_studies[i]) + "\n")
            raise e


if __name__ == "__main__":
    main()
