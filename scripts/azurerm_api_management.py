# azurerm_api_management
def azurerm_api_management(crf,cde,crg,headers,requests,sub,json,az2tfmess,cldurl):
    tfp="azurerm_api_management"
    tcode="640-"
    azr=""
    
    if crf in tfp:
    # REST or cli
        # print "REST Function App"
        url="https://" + cldurl + "/subscriptions/" + sub + "/providers/Microsoft.ApiManagement/service"
        params = {'api-version': '2019-01-01'}
        r = requests.get(url, headers=headers, params=params)
        try:
            azr= r.json()["value"]
        except KeyError:
            print ("Skipping api_management for now...")
            return
        tfrmf=tcode+tfp+"-staterm.sh"
        tfimf=tcode+tfp+"-stateimp.sh"
        tfrm=open(tfrmf, 'a')
        tfim=open(tfimf, 'a')
        print ("# " + tfp,)
        count=len(azr)
        print (count)
        for i in range(0, count):

            
            name=azr[i]["name"]
            loc=azr[i]["location"]
            id=azr[i]["id"]
            rg=id.split("/")[4].replace(".","-").lower()
            if rg[0].isdigit(): rg="rg_"+rg
            rgs=id.split("/")[4]
            if crg is not None:
                if rgs.lower() != crg.lower():
                    continue  # back to for
            if cde:
                print(json.dumps(azr[i], indent=4, separators=(',', ': ')))
            
            rname=name.replace(".","-")
            prefix=tfp+"."+rg+'__'+rname
            #print prefix
            rfilename=prefix+".tf"
            fr=open(rfilename, 'w')
            fr.write(az2tfmess)
            fr.write('resource ' + tfp + ' ' + rg + '__' + rname + ' {\n')
            fr.write('\t name = "' + name + '"\n')
            fr.write('\t location = "'+ loc + '"\n')
            fr.write('\t resource_group_name = "'+ rgs + '"\n')

            pubn=azr[i]["properties"]["publisherName"]
            pube=azr[i]["properties"]["publisherEmail"]
            skun=azr[i]["sku"]["name"]
            skuc=azr[i]["sku"]["capacity"]

            fr.write('\t publisher_name = "'+ pubn + '"\n')
            fr.write('\t publisher_email = "'+ pube + '"\n')
            fr.write('sku  { \n')
            fr.write('\t name = "'+ skun + '"\n')
            fr.write('\t capacity = "'+ str(skuc) + '"\n')
            fr.write('} \n')

    # tags block       
            try:
                mtags=azr[i]["tags"]
                fr.write('tags = { \n')
                for key in mtags.keys():
                    tval=mtags[key]
                    fr.write(('\t "' + key + '"="' + tval + '"\n'))
                fr.write('}\n')
            except KeyError:
                pass

            fr.write('}\n') 
            fr.close()   # close .tf file

            if cde:
                with open(rfilename) as f: 
                    print (f.read())

            tfrm.write('terraform state rm '+tfp+'.'+rg+'__'+rname + '\n')

            tfim.write('echo "importing ' + str(i) + ' of ' + str(count-1) + '"' + '\n')
            tfcomm='terraform import '+tfp+'.'+rg+'__'+rname+' '+id+'\n'
            tfim.write(tfcomm)  

        # end for i loop

        tfrm.close()
        tfim.close()
    #end stub
