import requests
url_age = "https://api.agify.io/"
url_gender = "https://api.genderize.io/"
url_nation = "https://api.nationalize.io/"
url_ip = "https://api.ipify.org/?format=json"
url_loc = "https://ipinfo.io/37.110.64.175/geo"
success = 0
ip = None


def ask_user():
    global success
    answer = input("предположение верно?(y/n)")
    if answer == "y":
        success += 1
        return True
    else:
        return False


def parse_probability(a):
    return int(a * 100)


def ask_age(n):
    r_age = requests.get(url_age, {"name": n})
    print(f"ваш предпологаемый возраст {r_age.json()['age']}")
    ask_user()


def ask_gender(n):
    r_gender = requests.get(url_gender, {"name": n})
    gender_data = r_gender.json()
    gender = "мужской" if gender_data["gender"] == "male" else "женский"
    probability = parse_probability(gender_data["probability"])
    print(f"ваш предпологаемый пол {gender} (точность {probability}%)")
    ask_user()


def ask_nation(n):
    global success
    r_nation = requests.get(url_nation, {"name": n})
    nation_data = r_nation.json()
    countries = nation_data['country']
    country_id = None
    country_probability = None
    countries_end = True

    for country in countries:
        current_country_id = country['country_id']
        current_country_probability = country['probability']
        if country_id is None and country_probability is None:
            country_id = current_country_id
            country_probability = current_country_probability
        elif country_probability < current_country_probability:
            country_probability = current_country_probability
            country_id = current_country_id
        print(f"ваша предпологаемая страна - {current_country_id}, вероятность  - {parse_probability(current_country_probability)}%")
        result = ask_user()
        if result:
            countries_end = False
            break

    if countries_end:
        print(
            f"вы не выбрали страну, с наибольшей вероятностью ({parse_probability(country_probability)}%) ваша страна - {country_id}")
        success += 1


def\
          k_ip():
    global ip
    response = requests.get(url_ip)
    ip = response.json()['ip']
    print(f"ваш предпологаемый ip адрес : {ip}")
    ask_user()


def ask_ip(n):
    global success
    r_loc = requests.get(url_loc, {"ip": n})
    print(f"ваши предпологаемые координаты : {r_loc.json()['loc']}")
    r_city = requests.get(url_loc, {"ip": n})
    print(f"ваш предпологаемый город - {r_city.json()['city']}")
    r_post = requests.get(url_loc, {"ip": n})
    print(f"ваш предпологаемый почтовый индекс - {r_post.json()['postal']}")
    r_ip_country = requests.get(url_loc, {"ip": n})
    print(f"ваша страна по ip - {r_ip_country.json()['country']}")
    ask_user()



def detected():
    global ip
    url = f"https://ipinfo.io/{ip}/geo"
    response = requests.get(url)
    print(response.json())


if __name__ == '__main__':
    name = input("введите ваше имя:")

    questions = [
        ask_age(name),
        ask_gender(name),
        ask_nation(name),
        ask_ip(ip),
        detected(),
    ]

    print(f"успешно угадано {success} из {len(questions)}")


