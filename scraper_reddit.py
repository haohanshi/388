from bs4 import BeautifulSoup
import requests
from time import sleep
import json

def getreddit(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")
    set = soup.findAll("p")
    count = 0
    result = []
    for i in set:
        if i.attrs == {}:
            if i.string != None:
                if len(i.string) > 25:
                    count += 1
                    if count > 10:
                        result.append(i.string)
    return result
def reddit():
    urllist = ["https://www.reddit.com/r/Debate/comments/5hdv8q/need_advice_on_how_to_get_a_state_point_fast/?st=iwimece7&sh=b09d8fa0",
               "https://www.reddit.com/r/Debate/comments/5go4e2/between_rounds_do_you_work_on_debate_or_just_sit/?st=iwimw0uo&sh=98259779",
               "https://www.reddit.com/r/Debate/comments/5gj344/event_sizes_at_local_tournaments/?st=iwimxa3y&sh=40e87e8e",
               "https://www.reddit.com/r/Debate/comments/5gfmsr/new_at_this_debate_coming_up/?st=iwimy0cv&sh=b70e6b40",
               "https://www.reddit.com/r/Debate/comments/5gbejt/when_you_find_the_super_secret_pro_argument/?st=iwimyp6t&sh=a973337a",
               "https://www.reddit.com/r/Debate/comments/5gd374/worst_reasons_for_losing_a_round/?st=iwimzaak&sh=b1885b55",
               "https://www.reddit.com/r/Debate/comments/5g4yrd/can_you_use_prep_time_to_relax_or_do_you_have_to/?st=iwin001s&sh=4d1d66e5",
               "https://www.reddit.com/r/Debate/comments/5g53x1/january_topic_where_do_we_draw_the_line/?st=iwin0cg4&sh=86fbc6c4",
               "https://www.reddit.com/r/Debate/comments/5fyng4/huge_changes_to_rpfc/?st=iwin1z6w&sh=19542284",
               "https://www.reddit.com/r/Debate/comments/5fins3/friends_dont_let_friends/?st=iwin36j2&sh=971592f1",
               "https://www.reddit.com/r/Debate/comments/5f6jdb/cocaine_good/?st=iwin46xy&sh=e506e045",
               "https://www.reddit.com/r/Debate/comments/5f203w/the_farccolombia_peace_deal_on_1124_appears_to_be/?st=iwin4xwx&sh=5e5c1cfb",
               "https://www.reddit.com/r/Debate/comments/5ealu7/worst_way_you_have_been_judge_screwed_in_a_round/?st=iwin6u2t&sh=debad97b",
               "https://www.reddit.com/r/Debate/comments/5e1c4h/what_do_i_do_if_my_opponent_entirely_misstates/?st=iwin7hie&sh=e47e4623",
               "https://www.reddit.com/r/Debate/comments/5djqn2/weird_debate_arguments_part_the_second/?st=iwin85bt&sh=0d874041",
               "https://www.reddit.com/r/Debate/comments/5ddhya/argument_against_status_quo_framework/?st=iwink4mp&sh=92adb29b",
               "https://www.reddit.com/r/Debate/comments/5d6yaz/the_nsda_doesnt_believe_in_integrity/?st=iwinkkf4&sh=e69841a1",
               "https://www.reddit.com/r/Debate/comments/5cysri/what_makes_it_to_finals_more_stock_or_unique/?st=iwinl4cq&sh=41aea921",
               "https://www.reddit.com/r/Debate/comments/5cie6y/how_to_be_a_better_second_speaker_pf/?st=iwinmq0a&sh=da8f9fa7",
               "https://www.reddit.com/r/Debate/comments/5chmrd/how_many_pages_of_counters_do_you_usually_have_pf/?st=iwinnbfn&sh=45ec861d",
               "https://www.reddit.com/r/Debate/comments/5cfo8r/what_exactly_is_the_internet_of_things/?st=iwinnlvh&sh=7f15655c",
               "https://www.reddit.com/r/Debate/comments/5c1n8y/donald_trump_has_been_elected_president_discuss/?st=iwinozkx&sh=6596863d",
               "https://www.reddit.com/r/Debate/comments/5bt9d9/resolved_the_united_states_should_end_plan/?st=iwinpik4&sh=386c8f35",
               "https://www.reddit.com/r/Debate/comments/5bhop2/how_to_not_burn_out/?st=iwinqik4&sh=4b85855a",
               "https://www.reddit.com/r/Debate/comments/5ayk7t/addiction_to_debate_research/?st=iwinrcst&sh=ba6b70b6"]
    result = []
    for url in urllist:
        r = getreddit(url)
        while r == []:
            print "while"
            sleep(5)    
            r = getreddit(url)
        print "get content from ", url
        result = result + r
    return result

with open ("reddit_debate.json", "w") as wf:
    print("start collecting data...")
    result = reddit()
    json.dump(result, wf)


            

    

