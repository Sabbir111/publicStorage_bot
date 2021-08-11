from functions import *
from time import sleep
import math
import threading


def main():
    links = search_for_link()["data"]
    links_length = len(links)
    # print(links_length)
    if links_length == 0:
        print("links not available")
    else:
        limited_links = 2000
        link_list_number = links_length / limited_links
        link_list_number = int(math.ceil(link_list_number))
        # print(link_list_number)

        list_of_list = multi_list(link_list_number)["data"]
        # print(list_of_list)
        if not list_of_list:
            print("no links available")
        else:
            for i in range(link_list_number):
                links_List = list_of_list[0]
                browserThread = threading.Thread(target=runBot, args=(links_List,))
                browserThread.start()
                list_of_list.pop(0)


def schedule():
    while True:
        main()
        print("sleep for 24 hours.")
        sleep(86400)


schedule()

