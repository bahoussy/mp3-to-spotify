
import json
import os
from Secrets import id,token,secret
import requests
import webbrowser
import spotipy

class CreatePlalist:
    def __init__(self):
        self.user_id = id
        self.user_token= token
        self.secret = secret



    def get_auth(self):
        scope = 'user-library-read'
        username=input("username: ")
        x = spotipy.prompt_for_user_token(username,scope,client_id=id,client_secret=secret,redirect_uri="http://127.0.0.1/spotAPI/index.html")
        print(x)
        self.user_token = x
        '''url = "http://127.0.0.1/index.html"

        query = "https://accounts.spotify.com/authorize?client_id={}&response_type=code&redirect_uri={}".format(id,url)

        response = requests.get(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.user_token)
            }
        )
        webbrowser.open(query,new=2)

'''

    def getting_files(self,directory):
        file_names = []
        for filename in os.listdir(directory):
            file_names.append(filename)

        return file_names

    def create_playlist(self,name):
        request_body = json.dumps({
            "name": "{}".format(name),
            "description":"eksdee",
            "public":True
        }
        )
        query = "https://api.spotify.com/v1/users/{}/playlists".format(self.user_id)
        response = requests.post(
            query,
            data = request_body,
            headers={
                "Content-Type":"application/json",
                "Authorization":"Bearer {}".format(self.user_token)
            }
        )
        response_json = response.json()


        return response_json['id']

    def add_to_playlist(self, playlist_id,uri):
        query = "https://api.spotify.com/v1/playlists/{}/tracks?uris={}".format(
            playlist_id,uri)

        response = requests.post(
            query,
            data=uri,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.user_token)
            }
        )

        # check for valid response status
       # print(response)

    def search(self,query):
        query = "https://api.spotify.com/v1/search?q={}&type=track".format(query)



        response = requests.get(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.user_token)
            }
        )
        response_json = response.json()

        songs = response_json["tracks"]["items"]
        uri =""
        try:
            uri = songs[0]["uri"]
        except:
            pass

        return uri
    def search_artist(self,query):
        query = "https://api.spotify.com/v1/search?q={}&type=artist".format(query)
        response = requests.get(
            query,
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(self.user_token)
        }
        )
        response_json = response.json()
        artist_id = response_json["artists"]["items"][0]["id"]
        return artist_id

    def get_related(self, ids):
        query = "https://api.spotify.com/v1/artists/{}/related-artists".format(ids)
        response = requests.get(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.user_token)
            }
        )
        response_json = response.json()
        artist_id = response_json["artists"][0]["id"]
        return artist_id

    def get_top_related(self,ids):
        query="https://api.spotify.com/v1/artists/{}/top-tracks?country=PT".format(ids)
        response = requests.get(
            query,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.user_token)
            }
        )
        response_json = response.json()
        related_track = response_json["tracks"][0]["id"]

        query2 = "https://api.spotify.com/v1/tracks/{}".format(related_track)
        response2 = requests.get(
            query2,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.user_token)
            }
        )
        response2_json = response2.json()
        related_track2 = response2_json["uri"]

        return related_track2

    def main(self):
        self.get_auth()
        unique_uri = []
        directory = input("Where is your folder located?")
        files =self.getting_files(directory)
        playlist_name = input("What is the name of the playlist?")
        p_id = self.create_playlist(playlist_name)
        rp_id = self.create_playlist("Related to - {}".format(playlist_name))
        for f in files:
            try:
                split_names = f.split("-")
                query = split_names[1].split("(")
                q = query[0].split(".")
                qa = split_names[0]
                uri = self.search(q[0])
                self.add_to_playlist(p_id,uri)
            except:
                pass
            try:

                ids=self.search_artist(qa)
                i = self.get_related(ids)
                related = self.get_top_related(i)
                if unique_uri.__contains__(related):
                    pass
                else:
                    unique_uri.append(related)
                    self.add_to_playlist(rp_id,related)

            except:
                pass



if __name__ == "__main__":
    create = CreatePlalist()
    create.main()