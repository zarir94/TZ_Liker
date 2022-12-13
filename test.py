from Home.liker_helper import convert_to_dict, get_post_react_amount
from requests import get, post

cookie = "datr=R-eXY5YPgGPITMVe1Bau8azj; sb=R-eXY-HyadqDBT-V7KvqpcKF; m_pixel_ratio=1.84375; fr=0CtUwBpNrLSjRjvvP.AWVZpPD2NNnIIXYEEySwOJ1ZPpo.Bjl-dH.Q7.AAA.0.0.Bjl-dZ.AWW2ev3P7-4; c_user=100075924800901; xs=45%3Apj6SIZJz6kFWxw%3A2%3A1670899546%3A-1%3A5149; m_page_voice=100075924800901; wd=391x752; locale=en_GB; fbl_cs=AhC8FccwkuKSmD6k4l3omzFUGGdFY3lMOEtzb2N2N05JNmtGOD1LZndrcQ; fbl_ci=538158021535757; vpd=v1%3B752x391x1.84375; fbl_st=101127008%3BT%3A27848326"

print(get_post_react_amount('115570984317061', cookie))

# https://mbasic.facebook.com/ufi/reaction/profile/browser/fetch/?ft_ent_identifier=pfbid032QyGRFrbCFJzo1duTW5WL7BJ6wy43iHCFKauvkfR16zU5k9GsF5mDxWJ9toUhefml&limit=10&total_count=4146&paipv=0&eav=AfbiYKNJXzFzL85S1Mh2ZvKqhRiwkbv4FgqKY4SeWixiNpaLCU1yN-en9XWOQ35kjY0

# https://mbasic.facebook.com/ufi/reaction/profile/browser/fetch/?ft_ent_identifier=115570774317082&limit=10&total_count=4146&paipv=0&eav=AfaSDPtEWgKcnbtIbtBYJzuffQnUonXZAigZGLmQO4uauFa7vaScqj6Jqbq8rdchocY
