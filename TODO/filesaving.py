'''
    with open('files/datamining_{}.txt'.format(d), '{}'.format(schreibtyp)) as f:
            for items in testliste:
                for item in items:
                        letzteid = items[-1]['id_str']
                    #this
                    #if not 'RT' in item['text']:
                        print ("itemid: {}".format(item['id_str']))

                        global zaehler
                        f.write(str(zaehler)+"\n")
                        print(zaehler)
                        ts = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(item['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
                        f.write("{}".format(ts)+"\n")
                        f.write(item['id_str']+"\n")
                        f.write(item['user']['id_str']+"\n")
                        f.write("@"+item['user']['screen_name']+"\n")
                        f.write("retweetcount: "+str(item['retweet_count'])+"\n")
                        #f.write("favcount: "+str(item['favorite_count'])+"\n")
                        f.write(str(item['text'].encode('UTF-8'))[2:-1]+"\n\n")
                        zaehler += 1
                        if str(lastid) == str(letzteid):
                            return

'''
