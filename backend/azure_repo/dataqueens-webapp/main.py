from agents.completion import complete
from agents.embed import embed

if __name__ == '__main__':
    response = complete('27 years old, driving Tesla Y 2021')
    print(response.content)