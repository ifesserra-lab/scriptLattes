import sys
import os

# Ensure src is in pythonpath
sys.path.append(os.path.join(os.getcwd(), 'src'))

print("Importing entities...")
try:
    from eo_lib.domain.entities import Initiative
    from research_domain.domain.entities import ResearchGroup, Researcher, initiative_demandantes
    from sqlalchemy.inspection import inspect
except Exception as e:
    print(f"Import Error: {e}")
    sys.exit(1)

def check_relationships():
    print(f"\n--- Checking Initiative ({Initiative}) ---")
    mapper = inspect(Initiative)
    for rel in mapper.relationships:
        print(f" - {rel.key}: {rel.mapper.class_.__name__} (Target)")

    print(f"\n--- Checking ResearchGroup ({ResearchGroup}) ---")
    mapper = inspect(ResearchGroup)
    for rel in mapper.relationships:
        print(f" - {rel.key}: {rel.mapper.class_.__name__} (Target)")
        
    print(f"\n--- Checking Researcher ({Researcher}) ---")
    mapper = inspect(Researcher)
    for rel in mapper.relationships:
        print(f" - {rel.key}: {rel.mapper.class_.__name__} (Target)")

if __name__ == "__main__":
    check_relationships()
