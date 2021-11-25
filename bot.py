import logging
import pandas as pd

TOKEN = "2009649095:AAEYkXs8Xpx1HPzKAooxjIfOKd4trQOtJeM"

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def verify_registrations():
    unverified_df = pd.read_excel('file1.xlsx')
    unverified_usn_list = unverified_df['USN'].tolist()

    discrepant_usn_df = pd.read_excel('lod.xlsx')
    discrepant_usn_list = discrepant_usn_df['Done'].tolist()

    stripped_unverified_usn_list = [s.strip() for s in unverified_usn_list]

    discrepencies = list(set(stripped_unverified_usn_list).intersection(discrepant_usn_list))
    return discrepencies





def verify(update,context):

    with open("file1.xlsx",'wb') as f:
        context.bot.get_file(update.message.document).download(out = f)

    l = verify_registrations()

    if(len(l)==0):
        update.message.reply_text(
            'All verified'
        )

    else:
        update.message.reply_text(
            l
        )


def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    dispatcher.add_handler(MessageHandler(Filters.document.file_extension("xlsx"), verify))


    # Start the Bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()