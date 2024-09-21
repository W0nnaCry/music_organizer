#!/usr/bin/python3

from shutil import move 
import os
import shutil
import argparse


def get_performer(track, delimiter):
    if delimiter in track:
        return track.split(delimiter)[0].strip()
    else:
        return None

def split_by_performers(tracks, delimiter, unrecognized_tracks_directory_name, is_case_sensitive):
    splitted_tracks = {unrecognized_tracks_directory_name : []}
    for track in tracks:
        performer = get_performer(track, delimiter)
        if performer:
            if is_case_sensitive:
                if performer not in splitted_tracks:
                    splitted_tracks[performer] = []
                splitted_tracks[performer].append(track)
            else:
                performer_variation = performer
                for group_name, group_tracks in splitted_tracks.items():
                    if group_name.upper() == performer.upper():
                        performer_variation = group_name
                        break
                if performer_variation not in splitted_tracks:
                    splitted_tracks[performer_variation] = []
                splitted_tracks[performer_variation].append(track)
        else:
            splitted_tracks[unrecognized_tracks_directory_name].append(track)
    return splitted_tracks

def get_tracks(directory):
    entries = os.listdir(directory)
    tracks = []
    for entry in entries:
        if os.path.isfile(os.path.join(directory, entry)):
            tracks.append(entry)
    return tracks

def organize_tracks(track_groups, tracks_directory, output_directory, is_copy_mode, is_verbose):
    for group_name, group_tracks in track_groups.items():
        group_directory = os.path.join(output_directory, group_name)
        if not os.path.isdir(group_directory):
            os.mkdir(group_directory)
            if is_verbose:
                print('creating directory: \"' + group_directory + '\"')
        for track in group_tracks:
            track_path = os.path.join(tracks_directory, track)
            if is_copy_mode:
                if is_verbose:
                    print('copy track \"' + track_path + '\" to \"' + group_directory + '\"')
                shutil.copy(track_path, group_directory)
            else:
                if is_verbose:
                    print('move track \"' + track_path + '\" to \"' + group_directory + '\"')
                shutil.move(track_path, group_directory)

def review_track_groups(track_groups):
    for group_name, group_tracks in track_groups.items():
        print(group_name)
        for track in group_tracks:
            print('\t', track)
        print('\n')

def main():

    args_parser = argparse.ArgumentParser(
        prog='music_organizer', 
        description='Organize your music library',
        epilog='Have a fun'
    )
    default_music_directory = '.'
    args_parser.add_argument('-i', '--input', default=default_music_directory)
    args_parser.add_argument('-o', '--output', default=default_music_directory)
    args_parser.add_argument(
        '-c', '--copy', 
        action='store_true', 
        default=False, 
        help='copying tracks instead of moving'
    )
    args_parser.add_argument(
        '-s', '--casesens', 
        action='store_true', 
        default=False,
        help='enable case-sensitive performer determination'
    )
    args_parser.add_argument(
        '-u', '--unrecdir', default='other', 
        help='directory for tracks whose performer could not be determined'
    )
    args_parser.add_argument(
        '-d', '--delimiter', 
        default=' - ',
        help='delimiter used to determine track performer (default: \' - \')'
    )
    args_parser.add_argument('-v', '--verbose', action='store_true', default=False)
    args_parser.add_argument(
        '-r', '--review', action='store_true', default=False,
        help='only display produced organization tracks scheme, but do not write changes to file system'
    )
    
    args = args_parser.parse_args()
    
    input_directory = args.input
    output_directory = args.output
    unrecognized_tracks_directory_name = args.unrecdir
    delimiter = args.delimiter
    
    all_tracks = get_tracks(input_directory)
    track_groups = split_by_performers(all_tracks, delimiter, unrecognized_tracks_directory_name, args.casesens)

    if args.review:
        review_track_groups(track_groups)
    else:
        organize_tracks(track_groups, input_directory, output_directory, args.copy, args.verbose)

main()