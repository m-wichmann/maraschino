from flask import Flask, render_template
import jsonrpclib

from maraschino import app
from maraschino.noneditable import *
from maraschino.tools import *

@app.route('/xhr/recently_added/')
@requires_auth
def xhr_recently_added():
    return render_recently_added_episodes()


@app.route('/xhr/recently_added_movies/')
@requires_auth
def xhr_recently_added_movies():
    return render_recently_added_movies()


@app.route('/xhr/recently_added_albums/')
@requires_auth
def xhr_recently_added_albums():
    return render_recently_added_albums()


@app.route('/xhr/recently_added/<int:episode_offset>')
@requires_auth
def xhr_recently_added_episodes_offset(episode_offset):
    return render_recently_added_episodes(episode_offset)


@app.route('/xhr/recently_added_movies/<int:movie_offset>')
@requires_auth
def xhr_recently_added_movies_offset(movie_offset):
    return render_recently_added_movies(movie_offset)


@app.route('/xhr/recently_added_albums/<int:album_offset>')
@requires_auth
def xhr_recently_added_albums_offset(album_offset):
    return render_recently_added_albums(album_offset)

def render_recently_added_episodes(episode_offset=0):
    compact_view = get_setting_value('recently_added_compact') == '1'
    show_watched = get_setting_value('recently_added_watched_episodes') == '1'
    view_info = get_setting_value('recently_added_info') == '1'

    try:
        xbmc = jsonrpclib.Server(server_api_address())
        recently_added_episodes = get_recently_added_episodes(xbmc, episode_offset)

    except:
        recently_added_episodes = []

    return render_template('recently_added.html',
        recently_added_episodes = recently_added_episodes,
        episode_offset = episode_offset,
        compact_view = compact_view,
        total_episodes = total_episodes,
        view_info = view_info,
    )


def render_recently_added_movies(movie_offset=0):
    compact_view = get_setting_value('recently_added_movies_compact') == '1'
    show_watched = get_setting_value('recently_added_watched_movies') == '1'
    view_info = get_setting_value('recently_added_movies_info') == '1'

    try:
        xbmc = jsonrpclib.Server(server_api_address())
        recently_added_movies = get_recently_added_movies(xbmc, movie_offset)

    except:
        recently_added_movies = []

    return render_template('recently_added_movies.html',
        recently_added_movies = recently_added_movies,
        movie_offset = movie_offset,
        compact_view = compact_view,
        total_movies = total_movies,
        view_info = view_info,
    )


def render_recently_added_albums(album_offset=0):
    compact_view = get_setting_value('recently_added_albums_compact') == '1'
    view_info = get_setting_value('recently_added_albums_info') == '1'

    try:
        xbmc = jsonrpclib.Server(server_api_address())
        recently_added_albums = get_recently_added_albums(xbmc, album_offset)

    except:
        recently_added_albums = []

    return render_template('recently_added_albums.html',
        recently_added_albums = recently_added_albums,
        album_offset = album_offset,
        compact_view = compact_view,
        view_info = view_info,
    )


def get_num_recent_episodes():
    try:
        return int(get_setting_value('num_recent_episodes'))

    except:
        return 3

def get_num_recent_movies():
    try:
        return int(get_setting_value('num_recent_movies'))

    except:
        return 3


def get_num_recent_albums():
    try:
        return int(get_setting_value('num_recent_albums'))

    except:
        return 3


def get_recently_added_episodes(xbmc, episode_offset=0):
    num_recent_videos = get_num_recent_episodes()
    global total_episodes
    total_episodes = None

    try:
        recently_added_episodes = xbmc.VideoLibrary.GetRecentlyAddedEpisodes(properties = ['title', 'season', 'episode', 'showtitle', 'playcount', 'thumbnail'])['episodes']

        if get_setting_value('recently_added_watched_episodes') == '0':
            unwatched = []
            for episodes in recently_added_episodes:
                episode_playcount = episodes['playcount']

                if episode_playcount == 0:
                    unwatched.append(episodes)
                    total_episodes = len(unwatched)

            recently_added_episodes = unwatched[episode_offset:num_recent_videos + episode_offset]
        else:
            total_episodes = len(recently_added_episodes)
            recently_added_episodes = recently_added_episodes[episode_offset:num_recent_videos + episode_offset]

    except:
        recently_added_episodes = []

    return recently_added_episodes


def get_recently_added_movies(xbmc, movie_offset=0):
    num_recent_videos = get_num_recent_movies()
    global total_movies
    total_movies = None

    try:
        recently_added_movies = xbmc.VideoLibrary.GetRecentlyAddedMovies(properties = ['title', 'year', 'rating', 'playcount', 'thumbnail'])['movies']

        if get_setting_value('recently_added_watched_movies') == '0':
            unwatched = []
            for movies in recently_added_movies:
                movie_playcount = movies['playcount']

                if movie_playcount == 0:
                    unwatched.append(movies)
                    total_movies = len(unwatched)

            recently_added_movies = unwatched[movie_offset:num_recent_videos + movie_offset]
        else:
            total_movies = len(recently_added_movies)
            recently_added_movies = recently_added_movies[movie_offset:num_recent_videos + movie_offset]

    except:
        recently_added_movies = []

    return recently_added_movies

def get_recently_added_albums(xbmc, album_offset=0):
    num_recent_albums = get_num_recent_albums()

    try:
        recently_added_albums = xbmc.AudioLibrary.GetRecentlyAddedAlbums(properties = ['title', 'year', 'rating', 'artist', 'thumbnail'])

        recently_added_albums = recently_added_albums['albums'][album_offset:num_recent_albums + album_offset]

    except:
        recently_added_albums = []

    return recently_added_albums
