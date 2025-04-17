import pandas as pd
from random import shuffle


# To do: 
# - Find a better algorithmn than the greedy method that is being used.
#   -> Could implement an algorithm to match competencies and reach and average experience threshold
# - Update Project class to include the team assigned 
# - Add some Utility functions to view the database of employees, to see what competencies and roles are found, piechart
# - Create fail conditions for createTeam functions:
#   -> Can fail if out of employees availible, check before comparing to teamSize, except error
#   -> Create a dictionary with fallback competencies in place of "Scrum Master" and "Product Owner"

# A fazer:
# - Encontrar um algoritmo melhor do que o método ganancioso que está sendo usado.
# -> Implementar um algoritmo para corresponder competências e atingir o limite médio de experiência
# - Atualizar a classe Projeto para incluir a equipe atribuída
# - Adicionar algumas funções utilitárias para visualizar o banco de dados de funcionários, para ver quais competências e funções são encontradas, gráfico de pizza
# - Criar condições de falha para as funções createTeam:
# -> Pode falhar se não houver funcionários disponíveis, verificar antes de comparar com teamSize, except error
# -> Criar um dicionário com competências alternativas no lugar de "Scrum Master" e "Product Owner"

class Employee:
    def __init__(self, name: str, expInYear: int, roles: list, competencies: list):
        self.name = name
        self.expInYear = expInYear
        self.roles = roles
        self.competencies = competencies
        self.available = True

    def set_available(self, availablitly):
        self.available = availablitly
    
    def __str__(self):
        return f"{self.name}, ({self.expInYear} years of experience, \n     roles = {self.roles}, comp = {self.competencies})"

    def __repr__(self):
        return f"{self.name}, (Exp: {self.expInYear}, roles: {self.roles}, comp: {self.competencies})"

class Project:
    def __init__(self, projectTitle: str, requiredCompetencies: list, teamSize: int):
        self.projectTitle = projectTitle
        self.requiredCompetencies = requiredCompetencies
        self.teamSize = teamSize
        self.assignedTeam = None

    def __repr__(self):
        return f"Project: {self.projectTitle}, Required Competencies: {self.requiredCompetencies}"
    
class ScrumTeam:
    def __init__(self, teamProject: Project):
        self.teamProject = teamProject
        self.teamMembers = {"Scrum Master": None,
                            "Product Owner": None,
                            "Developers" : None
                            }
        
    def __repr__(self):
        return f"Scrum Team for Project: {self.teamProject.projectTitle}, Members: {self.teamMembers}"
        
    def createTeamGreedy(self, candidates: list[Employee]):
        
        majorRoles = {"Scrum Master": None,
                "Product Owner": None}
        developers = {}

        projectReq = self.teamProject.requiredCompetencies

        def findBestCandidates():
            availible = [c for c in candidates if c.available == True]
            bestCandidates = []

            for c in availible:
                for comp in c.competencies:
                    if comp in projectReq:
                        bestCandidates.append(c)
                        break

            return bestCandidates

        def findBestRole(role: str, bestCandidates):
            bestCandidate = None

            try: 
                bestCandidate = max([cand for cand in bestCandidates if role in cand.roles and cand.available], key=lambda x: x.expInYear)
            except:
                bestCandidate = max([cand for cand in candidates if role in cand.roles and cand.available], key=lambda x: x.expInYear)
            
            return bestCandidate

        bestCandidates = findBestCandidates()

        for role in majorRoles:
            chosenCandidate = findBestRole(role, bestCandidates)
            chosenCandidate.set_available(False)
            majorRoles[role] = chosenCandidate

        devsNeeded = self.teamProject.teamSize - len(majorRoles)

        selectedDevs = [dev for dev in bestCandidates if dev.available and "Developer" in dev.roles][:devsNeeded]

        if len(selectedDevs[:devsNeeded]) != devsNeeded:
            remainingDevs = devsNeeded - len(selectedDevs)
            for dev in selectedDevs:
                dev.set_available(False)
            possibleDevs = [dev for dev in candidates if dev.available and "Developer" in dev.roles]
            for i in range(remainingDevs):
                selectedDevs.append(possibleDevs[i])
                possibleDevs[i].set_available(False)
        
        developers = selectedDevs
        majorRoles.update({"Developers": developers})
        self.teamMembers.update(majorRoles)

    def createTeamRandom(self, candidates: list[Employee]):
        availible = [cand for cand in candidates if cand.available]
        shuffle(availible)
        self.teamMembers["Scrum Master"] = availible[0]
        self.teamMembers["Product Owner"] = availible[1]
        self.teamMembers["Developers"] = []
        for i in range(self.teamProject.teamSize - 2):
            self.teamMembers["Developers"].append(availible[i + 2])

    def printScrumTeam(self): 
            print(f"\nTeam for Project: {self.teamProject.projectTitle}, Team Size = {self.teamProject.teamSize}\n")
            print(f"--Scrum Master--\n{self.teamMembers["Scrum Master"]}")
            print(f"\n--Product Owner--\n{self.teamMembers["Product Owner"]}")  
            print(f"\n--Developers--")       
            for dev in self.teamMembers["Developers"]:
                print(f"{dev}")
            print()

def importEmployeesFromCSV(inputCSV):
    df = pd.read_excel(inputCSV)

    employees = []

    for  i, row in df.iterrows():
        empComp = row["Competencies"].split(",")
        empRole = row["Roles"].split(",")
        employees.append(Employee(row["Name"], row["YearsExperience"], empRole, empComp))
    
    return sorted(employees, key=lambda employee: employee.expInYear, reverse=True)

candidates = importEmployeesFromCSV("prototype/dataset/employees_scrum_db.xlsx")

projects = [Project("Project A", ["HTML", "Node.js"], 6),
            Project("Project B", ["HTML", "Python"], 8),
            Project("Project C", ["HTML", "Python"], 8),
            Project("Project D", ["Azure", "Docker", "Python"], 6),
            Project("Project E", ["AWS", "Mobile Dev"], 6),
            ]

# First three use greedy algorithm
for proj in projects[:3]:
    proj.assignedTeam = ScrumTeam(proj)
    proj.assignedTeam.createTeamGreedy(candidates)
    proj.assignedTeam.printScrumTeam()

    for i in range(2):
        print("-" * 40)

# Last two use random algorithm
for proj in projects[3:]:
    proj.assignedTeam = ScrumTeam(proj)
    proj.assignedTeam.createTeamRandom(candidates)
    proj.assignedTeam.printScrumTeam()

    for i in range(2):
        print("-" * 40)

