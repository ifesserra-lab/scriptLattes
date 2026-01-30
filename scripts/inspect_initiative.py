from eo_lib.domain.entities import Initiative
from research_domain.domain.entities import ResearchGroup, Researcher
from sqlalchemy.inspection import inspect

def check_relationships():
    print("Checking Initiative relationships:")
    mapper = inspect(Initiative)
    for rel in mapper.relationships:
        print(f" - {rel.key}: {rel.mapper.class_.__name__}")

    print("\nChecking ResearchGroup relationships:")
    mapper = inspect(ResearchGroup)
    for rel in mapper.relationships:
        print(f" - {rel.key}: {rel.mapper.class_.__name__}")
        
    print("\nChecking Researcher relationships:")
    mapper = inspect(Researcher)
    for rel in mapper.relationships:
        print(f" - {rel.key}: {rel.mapper.class_.__name__}")

if __name__ == "__main__":
    check_relationships()
