import pandas as pd
import argparse

from mnemosyne.script import Mnemosyne

def read_tsv(tsv_file: str) -> (pd.DataFrame, str):
    try:
        df = pd.read_csv(tsv_file, sep='\t')
        return df, None
    except FileNotFoundError:
        return None, "no such file: " + tsv_file
    except Exception as e:
        return None, "unknown error reading " + tsv_file + " : " + str(e)

def get_mnemosyne_db(data_dir: str) -> Mnemosyne:
    mnemosyne = Mnemosyne(data_dir)
    return mnemosyne


def compare_and_update(mnemosyne: Mnemosyne, tsv: pd.DataFrame, dry_run: bool):
    # tsv to dict with front as key
    new_cards = dict([(front, {'Back':back, 'Tags':tags}) for front, back, tags in zip(tsv['Front'], tsv['Back'], tsv['Tags'])])

    # Update existing cards
    for card_id, fact_id in mnemosyne.database().cards():
        card = mnemosyne.database().card(card_id, is_id_internal=True)
        if card.fact['f'] in new_cards:
            front = card.fact['f']
            back = card.fact['b']
            new_card = new_cards[front]
            new_back = new_card['Back']
            new_tags = new_card['Tags']
            if new_card['Back'] != back:
                update_card(mnemosyne, front, new_back, new_tags, dry_run)
            del new_cards[front]

    # Insert remaining cards
    for front in new_cards:
        back = new_cards[front]['Back']
        tags = new_cards[front]['Tags']
        insert_card(mnemosyne, front, back, tags, dry_run)

def update_card(mnemosyne: Mnemosyne, front: str, back: str, tags: list[str], dry_run: bool):
    print("Updating " + front)
    if dry_run:
        return

def insert_card(mnemosyne: Mnemosyne, front: str, back: str, tags: list[str], dry_run: bool):
    print("Inserting " + front)
    if dry_run:
        return


def main():
    args = parse_args()
    # 'data_dir = None' will use the default system location, edit as appropriate.
    mnemosyne = get_mnemosyne_db(args.data_dir)
    tsv, err = read_tsv(args.tsv)
    if err is not None:
        print(err)
        return
    compare_and_update(mnemosyne, tsv, args.dry_run)


def parse_args():
    parser=argparse.ArgumentParser(description="a script to do stuff")
    parser.add_argument("--data-dir", type=str, default="./data")
    parser.add_argument("--tsv", type=str, default="./test.tsv")
    parser.add_argument("--dry-run", type=bool, default=True)
    args=parser.parse_args()
    return args

if __name__ == '__main__':
    main()
