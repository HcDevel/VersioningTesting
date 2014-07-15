import urllib.request
import json

class update: #This class searches for updates. It only connects to GitHub, so you can be shure I do not collect any personal data
    def __init__ (self, auto_search=True, pre_releases=False):
        self.version = '1.0.2'
        self.available_update = {'compatible':None, 'incompatible':None}
        
        if (isinstance(auto_search, bool)):
            self.auto_search = auto_search
        else:
            raise Exception ('Auto search value has to be a boolean')
            
        if (isinstance(pre_releases, bool)):
            self.pre_releases = pre_releases
        else:
            raise Exception ('Pre release value has to be a boolean')
        
    def enable_automatic_search (self):
        self.auto_search = True
        
    def disable_automatic_search (self):
        self.auto_search = False
        
    def show_pre_releases(self):
        self.pre_releases = True
        
    def hide_pre_releases(self):
        self.pre_releases = False
        
    def search (self):
        self.available_update = {'compatible':None, 'incompatible':None}
        compare = int (self.version.replace('.', ''))
        
        try:
            releases = json.loads(urllib.request.urlopen('https://api.github.com/repos/HcDevel/VersioningTesting/releases').read().decode("utf-8")) #Get releases with the GitHub API (https://developer.github.com/v3/repos/releases/)
        except:
            print ('Connection to update server not possible')
            return (-1)
            
        releases = sorted(releases, key=lambda release: release['id']) #Chamge order by ID of release
        for release in releases[:]:
            if (compare < int (release['tag_name'].replace('.', ''))): #If remote version is newer
                release['compatible'] = release['body'].split('\r\n')[-1].lower().split(':') #Extract compatibility
                if (release['compatible'][0] == 'compatible'):
                    if (release['compatible'][1] == 'true' and self.available_update['incompatible'] == None):
                        if (release['prerelease'] == False or (self.pre_releases == True and release['prerelease'] == True)): #Check if release is stable
                            print (release['tag_name'])
                            self.available_update['compatible'] = release
                    else:
                        print ('incompatible')
                        if (self.available_update['incompatible'] == None or release['prerelease'] == False or (self.pre_releases == True and release['prerelease'] == True)): #Check if release is stable
                            self.available_update['incompatible'] = release
                else:
                    print ('Compatibility of ' + release['tag_name'] + ' can not be checked')
                    break
        
        if (self.pre_releases == False and self.available_update['incompatible'] != None and self.available_update['incompatible']['prerelease'] == True):
            self.available_update['incompatible'] = None
            
        return (self.available_update)
        
test = update ()
test.show_pre_releases()
test.hide_pre_releases()
print (test.search())