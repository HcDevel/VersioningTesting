import urllib.request
import json

class update: #This class searches for updates. It only connects to GitHub, so you can be shure I do not collect any personal data
    def __init__ (self, auto_search=True, pre_releases=False):
        self.version = '1.0.2'
        self.available_update = None
        
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
        compare = int (self.version.replace('.', ''))
        
        try:
            releases = json.loads(urllib.request.urlopen('https://api.github.com/repos/HcDevel/VersioningTesting/releases').read().decode("utf-8")) #Get releases with the GitHub API (https://developer.github.com/v3/repos/releases/)
        except:
            print ('Connection to update server not possible')
            return (-1)
            
        for release in releases[:]:
            if (compare < int (release['tag_name'].replace('.', ''))): #If remote version is newer
                if (release['prerelease'] == False or (self.pre_releases == True and release['prerelease'] == True)): #Check if release is stable
                    print ("found: " + release['tag_name'])
        
test = update ()
test.search()