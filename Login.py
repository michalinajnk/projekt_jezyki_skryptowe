import csv
import hashlib
import os

def make_pw_hash(password):
    return hashlib.sha256(str.encode(password)).hexdigest()


def check_pw_hash(password, hash):  #verify uer input
    if make_pw_hash(password) == hash:
        return True
    else:
        return False


class Game_Info:

    def __init__(self, csv_file):
        self.stored_users = self.stored_users(csv_file)

    def stored_users(self, csv_file):
        users = []
        with open(csv_file, 'r', encoding='UTF8') as f:
            reader = csv.reader(f)
            iter = 0
            for line in reader:
                if line != '\n':
                    if iter > 0:
                        if len(line) == 2:
                            users.append(User(line[0], line[1]))
                        elif len(line) == 3:
                            users.append(User(line[0], line[1], int(line[2])))
                    iter += 1
        return users

    def user_exist(self, login):
        for user in self.stored_users:
            if login == user.username:
                return True
        return False

    def usernames(self):
        usernames = []
        for user in self.stored_users:
            usernames.append(user.username)
        return usernames

    def get_user(self, login):
        for user in self.stored_users:
            if user.username == login:
                return user


    def get_user_hash_pass(self, usr):
        for user in self.stored_users:
            if user.username == usr:
                return user.hash_pass

    def get_user_best_score(self, usr):
        for user in self.stored_users:
            if user.username == usr:
                return user.best_score


class User:

    def __init__(self, usr_nm, h_pass, b_score=0):
        self.username = usr_nm
        self.hash_pass = h_pass
        self.best_score = b_score

    def __str__(self):
        return str(self.username) + 'score: ' + str(self.best_score)

    def update_score(self, new_score):
        if self.best_score < new_score:
            self.best_score = new_score

    def __eq__(self, other):
        return self.username == other.username

class Login:
    def __init__(self, login, game_info):
        self.hash_pass = game_info.get_user_hash_pass(login)

    def check_pass(self, password):



        print('SZUKAMY TEGO: ')
        print(self.hash_pass)
        print('MAMY TO:')
        print(make_pw_hash(password))

        if check_pw_hash(password, self.hash_pass):
            print('Correct password')
            return True
        else:
            return False


class Register:
    def __init__(self, login, password, game_info):
        self.salt = os.urandom(32)
        self.hash_pass = make_pw_hash(password)

        self.add_user('users.csv', login, self.hash_pass, game_info)


    def add_user(self, csv_file, login, hash_pass, game_info):
        if not game_info.user_exist(login):
            with open(csv_file, 'a', encoding='UTF8') as f:
                writer = csv.writer(f)
                writer.writerow([login, hash_pass, 0])



    def log_in(self, login, password, game_info):
        register = Register(login, password)
        for username in game_info.usernames():
            if username == login and register.salt == game_info.get_user_salt(login) and register.hash_pass == Game_Info.get_user_hash_pass(login):
                return True
        return False












