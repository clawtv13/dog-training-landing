#!/usr/bin/env python3
import json, os, requests

STORE=os.environ['SHOPIFY_STORE'].replace('https://','').rstrip('/')
CLIENT_ID=os.environ['SHOPIFY_CLIENT_ID']
CLIENT_SECRET=os.environ['SHOPIFY_CLIENT_SECRET']
API=os.environ.get('SHOPIFY_API_VERSION','2025-01')
THEME_ID='197989826891'


def token():
    r=requests.post(
        f'https://{STORE}/admin/oauth/access_token',
        headers={'Content-Type':'application/x-www-form-urlencoded'},
        data={'grant_type':'client_credentials','client_id':CLIENT_ID,'client_secret':CLIENT_SECRET},
        timeout=30,
    )
    r.raise_for_status()
    return r.json()['access_token']


def get_asset(tok,key):
    r=requests.get(f'https://{STORE}/admin/api/{API}/themes/{THEME_ID}/assets.json?asset[key]={key}',headers={'X-Shopify-Access-Token':tok},timeout=30)
    r.raise_for_status()
    return r.json()['asset']['value']


def put_asset(tok,key,value):
    r=requests.put(f'https://{STORE}/admin/api/{API}/themes/{THEME_ID}/assets.json',headers={'X-Shopify-Access-Token':tok,'Content-Type':'application/json'},json={'asset':{'key':key,'value':value}},timeout=30)
    r.raise_for_status()
    return r.json()


def main():
    tok=token()
    raw=get_asset(tok,'templates/index.json')
    data=json.loads(raw)
    sections=data['sections']

    # Hero
    hero=sections['image_banner_kWf976']
    hero['blocks']['heading_fGaJHG']['settings']['heading']='Cool Your Head. Calm Your Day.'
    hero['blocks']['text_XD6GTA']['settings']['text']='The Cooling Relief Cap delivers soothing cooling comfort around your forehead, temples, eyes, and head in seconds. Keep it chilled, pull it on, and reset whenever you feel overheated, tense, or overstimulated.'
    hero['blocks']['buttons_HpKcNj']['settings']['button_label_1']='Shop Cooling Relief Cap'
    hero['blocks']['buttons_HpKcNj']['settings']['button_link_1']='shopify://products/cooling-relief-cap'
    hero['blocks']['buttons_HpKcNj']['settings']['button_label_2']='See How It Works'
    hero['blocks']['buttons_HpKcNj']['settings']['button_link_2']='shopify://products/cooling-relief-cap'

    # top testimonials -> trust bar style
    t1=sections['testimonials_98gVhg']
    t1['settings']['title']='Trusted by customers who want a faster reset'
    t1['blocks']['column_z4Gan3']['settings']['title']='I keep mine in the fridge and grab it every evening after work.'
    t1['blocks']['column_z4Gan3']['settings']['author']='<em><strong>– Olivia C.</strong></em>'
    t1['blocks']['column_k3D7qn']['settings']['title']='The cooling effect around my temples and eyes is exactly what I wanted.'
    t1['blocks']['column_k3D7qn']['settings']['author']='<em><strong>— Daniel R.</strong></em>'

    # benefits
    m1=sections['multicolumn_cXTePr']
    m1['blocks']['column_dJtxXX']['settings']['title']='Fast Cooling Comfort'
    m1['blocks']['column_dJtxXX']['settings']['text']='<p>Enjoy a wraparound cooling feel when your head feels hot, tense, or overstimulated.</p>'
    m1['blocks']['column_GBWxRQ']['settings']['title']='Comfort + Light Blocking'
    m1['blocks']['column_GBWxRQ']['settings']['text']='<p>The soft stretch-fit design can cover the eyes to create a darker, calmer space to rest.</p>'
    m1['blocks']['column_WBrQj9']['settings']['title']='Reusable and Effortless'
    m1['blocks']['column_WBrQj9']['settings']['text']='<p>Store it in the fridge or freezer and use it again whenever you need a quick reset.</p>'

    # block 1
    i1=sections['image_with_text_pcnkW4']
    i1['blocks']['heading_m4WpN8']['settings']['heading']='A Simple Way to Cool Down and Switch Off'
    i1['blocks']['text_diXJzj']['settings']['text']='<p>Cooling Relief Cap is a soft gel-lined head cap designed to bring cooling comfort to the forehead, temples, eyes, and scalp. Pull it on straight from the fridge or freezer for an easy moment of relief at home, after work, or before bed.</p>'

    # block 2
    i2=sections['image_with_text_cD8aFG']
    i2['blocks']['heading_LzVJHW']['settings']['heading']='Made for the Moments You Need a Reset'
    i2['blocks']['text_F8BHCz']['settings']['text']='<p>Use it after long laptop sessions, overheated afternoons, stressful days, workouts, or whenever you want a darker, quieter, cooler break. It is a simple self-care tool for 10–20 minutes of calm.</p>'
    i2['blocks']['button_tzGHkL']['settings']['button_label']='Build Your Reset Routine'
    i2['blocks']['button_tzGHkL']['settings']['button_link']='shopify://products/cooling-relief-cap'

    # how it works section
    m2=sections['multicolumn_B7G8er']
    m2['settings']['title']='How It Works'
    m2['blocks']['column_YgYKtX']['settings']['title']='Chill It'
    m2['blocks']['column_YgYKtX']['settings']['text']='<p>Place it in the refrigerator or freezer for at least 10 minutes.</p>'
    m2['blocks']['column_3eBpyX']['settings']['title']='Pull It On'
    m2['blocks']['column_3eBpyX']['settings']['text']='<p>Wear it over the forehead, temples, eyes, and head for a wraparound cooling feel.</p>'
    m2['blocks']['column_HMJhUH']['settings']['title']='Reset'
    m2['blocks']['column_HMJhUH']['settings']['text']='<p>Relax for 10–20 minutes and let the cooling compression help you unwind.</p>'

    # why shoppers like it
    i3=sections['image_with_text_97Y4q6']
    i3['blocks']['heading_rHJ7YP']['settings']['heading']='Easy Relief Without Cords, Noise, or Fuss'
    i3['blocks']['text_hatGXC']['settings']['text']='<p>No charging. No cables. No complicated setup. Just chill it, wear it, and relax. The reusable design makes it easy to keep on hand for daily wind-downs, travel, or quick comfort whenever you need it.</p>'

    # testimonials
    t2=sections['testimonials_Q8MNin']
    t2['settings']['title']='What Customers Love About It'
    t2['blocks']['column_hhiJaN']['settings']['title']='I keep mine ready in the fridge.'
    t2['blocks']['column_hhiJaN']['settings']['text']='<p>It has become part of my nighttime routine whenever I need to unwind fast.</p>'
    t2['blocks']['column_hhiJaN']['settings']['author']='<em><strong>— Jason L.</strong></em>'
    t2['blocks']['column_ydgCfM']['settings']['title']='Super easy to use, and I love that it blocks light while I rest.'
    t2['blocks']['column_ydgCfM']['settings']['text']='<p>The cooling effect around my temples and eyes is exactly what I wanted after long screen days.</p>'
    t2['blocks']['column_ydgCfM']['settings']['author']='<em><strong>— Sarah M.</strong></em>'
    t2['blocks']['column_kkE7JU']['settings']['title']='No cords, no noise, no effort.'
    t2['blocks']['column_kkE7JU']['settings']['text']='<p>Perfect for hot days, stressful afternoons, and those moments when I just need 15 minutes to reset.</p>'
    t2['blocks']['column_kkE7JU']['settings']['author']='<em><strong>— Mark T.</strong></em>'

    # rich text mid
    r1=sections['rich_text_wM9LBi']
    r1['blocks']['heading_9kB93L']['settings']['heading']='Some days you just need cold, quiet, and 15 minutes to yourself.'
    r1['blocks']['text_Tdqmd7']['settings']['text']='<p>Cooling Relief Cap is built for exactly that.</p>'

    # lower testimonials
    t3=sections['testimonials_DkVD8h']
    t3['settings']['title']='People Who Tried It Keep Reaching For It'
    t3['blocks']['column_ikrKcR']['settings']['title']='I bought it for overheated, stressful afternoons.'
    t3['blocks']['column_ikrKcR']['settings']['text']='<p>Now I use it after work, after workouts, and before bed. It is simple, but it works.</p>'
    t3['blocks']['column_ikrKcR']['settings']['author']='<em><strong>— Laura D.</strong></em>'
    t3['blocks']['column_pWMCAM']['settings']['title']='It feels way better than juggling ice packs.'
    t3['blocks']['column_pWMCAM']['settings']['text']='<p>Much easier, less messy, and actually comfortable enough to keep using.</p>'
    t3['blocks']['column_pWMCAM']['settings']['author']='<em><strong>— Nina P.</strong></em>'

    # final CTA
    r2=sections['rich_text_8zt9VY']
    r2['blocks']['heading_drqpDk']['settings']['heading']='Ready for a Cooler, Calmer Reset?'
    r2['blocks']['text_AwCr4i']['settings']['text']='<p>Keep your Cooling Relief Cap chilled and ready whenever you need quick comfort, quiet, and a break from the heat.</p>'
    r2['blocks']['button_bfYXFJ']['settings']['button_label']='Shop Cooling Relief Cap'
    r2['blocks']['button_bfYXFJ']['settings']['button_link']='shopify://products/cooling-relief-cap'

    out=json.dumps(data, ensure_ascii=False, indent=2)
    put_asset(tok,'templates/index.json',out)
    print('homepage rewritten')

if __name__=='__main__':
    main()
