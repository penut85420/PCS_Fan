import re
import os
from tracking.riots import get_match_by_match_id, get_pros_match_team
from tracking.utils import mk_players_html, load, dump, mk_match_info

def main():
    replay_records = {}

    if os.path.exists('data/replay.json'):
        replay_records = load('data/replay.json')

    wsl_replays_dir = os.getenv('WSL_RP_DIR')
    windows_game_path = os.getenv('WIN_GAME_DIR')
    windows_replays_dir = os.getenv('WIN_RP_DIR')

    for _, _, file_list in os.walk(wsl_replays_dir):
        for file_name in sorted(file_list):
            match_id = re.search('\-(\d+)\.', file_name).group(1)
            if match_id in replay_records:
                print(f'{match_id} Skipped!')
                continue

            match = get_match_by_match_id(match_id)
            game_dur = match['gameDuration']
            game_dur_mins = game_dur // 60
            game_dur_secs = game_dur % 60
            time = f'{game_dur_mins:02d}:{game_dur_secs:02d}'
            print(f'\nWatching {match_id} - Time: {time}')
            team_side = get_pros_match_team(match)
            print(mk_match_info(team_side))
            mk_players_html(team_side, file_name)

            spec_cmd = (
                f'"{windows_game_path}" '
                f'"{windows_replays_dir}/{file_name}" '
                f'"-Locale=zh_TW"'
            )
            os.system(f'echo \'{spec_cmd}\' | clip.exe')
            print('Spector Command Copied!')

            replay_records[match_id] = team_side
            dump(replay_records, 'data/replay.json')
            redo = input('[Enter] Next [^C] Exit [K] Keep [S] Skip > ').strip()

            if redo == 'k':
                del replay_records[match_id]
                print(f'Record of {match_id} deleted')
                dump(replay_records, 'data/replay.json')
                print('\nBye!')
                exit(0)
            elif redo == 's':
                del replay_records[match_id]
                print(f'Record of {match_id} deleted')
                dump(replay_records, 'data/replay.json')

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\n\nBye!')
