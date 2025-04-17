import pandas as pd
import random
from faker import Faker

# Initialize faker and seed for reproducibility
fake = Faker()
random.seed(42)

# Configuration
num_employees = 500 # Number of Employees to Generate
num_comp_min = 2 # Number of min competencies
num_comp_max = 4 # Number of max competencies

roles_pool = ["Developer", "Scrum Master", "Product Owner"]

competencies_pool = [
    "Python", "Java", "React", "Node.js", "Scrum", "Agile", "DevOps",
    "UX", "UI/UX", "Domain Knowledge", "HTML", "CSS", "JavaScript",
    "Spring Boot", "Kubernetes", "Docker", "MongoDB", "SQL", 
    "Product Vision", "Team Leadership", "Product Strategy",
    "Conflict Resolution", "Facilitation", "Marketing", "User Research",
    "Cloud Architecture", "AWS", "Azure", "GCP", "Machine Learning", 
    "Data Analysis", "CI/CD", "Security", "Testing", "Business Analysis",
    "Systems Thinking", "API Design", "REST", "GraphQL", "Data Engineering",
    "NoSQL", "PostgreSQL", "Communication", "Stakeholder Management",
    "Risk Management", "Budgeting", "Analytics", "Mobile Dev",
    "iOS", "Android", "Cross-functional Collaboration", "Project Management"
]

# Generate unique names
names = set()
while len(names) < num_employees:
    names.add(fake.name())

# Build employee records
employees_data = []
for name in names:
    years_exp = random.randint(1, 10)
    roles = random.sample(roles_pool, random.randint(1, 2))
    competencies = random.sample(competencies_pool, random.randint(num_comp_min, num_comp_max))
    employees_data.append([name, years_exp, ",".join(roles), ",".join(competencies)])

# Create DataFrame
df = pd.DataFrame(employees_data, columns=["Name", "YearsExperience", "Roles", "Competencies"])

# Export to Excel
output_path = f"prototype/dataset/employees_scrum_db_{num_employees}.xlsx"
df.to_excel(output_path, index=False)

print(f"Employee database saved to: {output_path}")
