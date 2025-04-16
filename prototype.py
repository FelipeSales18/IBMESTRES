import pandas as pd


#TODO
#1 - Define classe, employee (name, years of experience, roles, competencies, isInTeam(bool))
#                   project (project title, required competencies, priority)
#2 - create function to get all candidates and competencies from a csv file
#3 - create a function to sort through a list employees to find the best candidate for a role
#4 - create a function to form a project team

class Employee:
    def __init__(self, name: str, expInYear: int, roles: list, competencies: list):
        self.name = name
        self.expInYear = expInYear
        self.roles = roles
        self.competencies = competencies
        self.available = True

    def set_available(self, availablitly):
        self.available = availablitly

    def __repr__(self):
        return f"{self.name}, ({self.expInYear} years of experience, \n     roles = {self.roles}, comp = {self.competencies})"


class Project:
    def __init__(self, projectTitle: str, requiredCompetencies: list):
        self.projectTitle = projectTitle
        self.requiredCompetencies = requiredCompetencies

    def __repr__(self):
        return f"Project: {self.projectTitle}\nRequired Competencies = {self.requiredCompetencies}"


def importEmployeesFromCSV(inputCSV):
    df = pd.read_excel(inputCSV)

    employees = []

    for  i, row in df.iterrows():
        empComp = row[2].split(",")
        empRole = row[3].split(",")
        employees.append(Employee(row[0], row[1], empComp, empRole))
    
    return sorted(employees, key=lambda employee: employee.expInYear, reverse=True)

def makeScrumTeam(project: Project, candidates: list[Employee], teamSize: int):
    
    majorRoles = {"Scrum Master": None,
            "Product Owner": None}
    developers = []

    projectReq = project.requiredCompetencies


    def findBestCandidates():
        availible = [c for c in candidates if c.available == True]
        bestCandidates = []
        for candidate in availible:
            for comp in candidate.competencies:
                if comp in projectReq:
                    bestCandidates.append(candidate)
                    break
        
        return bestCandidates
        print(bestCandidates)

    def findBestRole(role: str, bestCandidates):
        bestCandidate = None

        # Try first in bestCandidates
        for cand in bestCandidates:
            if role in cand.roles:
                if bestCandidate == None:
                    bestCandidate = cand
                elif cand.expInYear > bestCandidate.expInYear:
                    bestCandidate = cand
                
        if bestCandidate != None:
            return bestCandidate
   
        for cand in candidates:
            if role in cand.roles:
                if bestCandidate == None:
                    bestCandidate = cand
                elif cand.expInYear > bestCandidate.expInYear:
                    bestCandidate = cand
        
        return bestCandidate
    


    def printScrumTeam():

        print(f"\nTeam for Project: {project.projectTitle}\n")
        print(f"--Scrum Master--\n{majorRoles['Scrum Master']}")
        print(f"\n--Product Owner--\n{majorRoles['Product Owner']}")  
        print(f"\n--Developers--")       
        for dev in developers:
            print(f"{dev}")
    


    bestCandidates = findBestCandidates()

    for role in majorRoles:
        majorRoles[role] = findBestRole(role, bestCandidates)
        majorRoles[role].set_available(False)

    devsNeeded = teamSize - len(majorRoles)

    for possibleDev in bestCandidates:
        if len(developers) < devsNeeded:
            if possibleDev.available == True and "Developer" in possibleDev.roles:
                developers.append(possibleDev)
                possibleDev.set_available(False)
        else:
            break
        
    if len(developers) != devsNeeded:
        for possibleDev in candidates:
            if possibleDev.available == True and "Developer" in possibleDev.roles:
                developers.append(possibleDev)
                possibleDev.set_available(False)
    
    printScrumTeam()







candidates = importEmployeesFromCSV("employees_scrum_db.xlsx")

project = Project("Website", ["Node.js", "HTML"])

#for i in range(5):
#    print(candidates[i])

makeScrumTeam(project=project, candidates=candidates, teamSize = 6)
