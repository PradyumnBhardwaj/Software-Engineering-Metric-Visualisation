import json
import requests
from github import Github
from pprint import pprint
import pygal

URL = "https://api.github.com/search/repositories?q="  # The basic URL to use the GitHub API

def getUrl(url):
    """ Given a URL it returns its body """
    response = requests.get(url)
    return response.json()
#Enter the Github username of the user you wish to see data
github_username = input("Enter Github Username: ")

try:
    personal_token = input("Enter your personal access token(PAT): ")
    git_data = Github(personal_token)
    user_github = git_data.get_user(github_username)
    print("Access Granted")
    print("User data is being analysed")
except:
    git_data = Github()
    user_github = git_data.get_user(github_username)
    print("Access not granted")
#Get Repositories Data
repositories = user_github.get_repos()

print("This might take some time")

#I have represented the repositories
#a user has made each month
#using a bar graph
no_of_months= [0] * 12
Months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
for rep in repositories:
 month = int(rep.created_at.strftime("%m"))
 #counting the number of repositories made each day
 no_of_months[month-1] = no_of_months[month-1] + 1

bar_chart = pygal.Bar()
bar_chart.title = f"Repositories made by {user_github.login} each month"
bar_chart.x_labels = Months
bar_chart.add('', no_of_months)
bar_chart.render_to_file("Repositories_per_month.svg")

#I have represented the languages
#a user has used
#using a pie chart

languages_used = {}
for rep in repositories:
    language = rep.language
    #counting the total number of languages
    if language in languages_used:
        languages_used[language] = languages_used[language] + 1
    else:
        languages_used[language] = 1
   
pie_chart = pygal.Pie()
pie_chart.title = f"{user_github.login}'s most frequent coding languages"
for language in languages_used:
    pie_chart.add(language, languages_used[language])
pie_chart.render_to_file("Languages_used_by_user.svg")

#I have represented the number of times 
#a repository is starred by the user 
#using a stacked line chart
Y_label="Count of repositories"
line_chart = pygal.StackedLine(fill=True)
line_chart.title = f"Starred repositories of {user_github.login}"
for rep in repositories:
 line_chart.add(rep.name, rep.stargazers_count)
 line_chart.render_to_file("Starred_repositories_of_user.svg")

print("Metrics are saved on your local device")

