from twittervotes.core.cmdline_parser import parse_commandline_args
from twittervotes.core import execute_request
from twittervotes.core.twitter.hashtagstats_manager import Runner

import threadsafe_tkinter
from threadsafe_tkinter import Frame
from threadsafe_tkinter import Label
from threadsafe_tkinter import StringVar
from threadsafe_tkinter.ttk import Button

class Application(Frame):

    def __init__(self, hashtags=[], master=None):
        super().__init__(master)

        self._manager = Runner(self._on_success,
                               self._on_error,
                               self._on_complete)

        self._items = {hashtag: StringVar() for hashtag in hashtags}
        self.set_header()
        self.create_labels()
        self.pack()

        self.button = Button(self,style='start.IButton',
                             text='Update',
                             command=self._fetch_data)
        self.button.pack(side="bottom")

    def set_header(self):
        title = Label(self,
                      text='Voting for hashtags',
                      font=("Helvetica", 24),
                      height=4)
        title.pack()

    def create_labels(self):
        for key, value in self._items.items():
            label = Label(self,
                          textvariable=value,
                          font=("Helvetica", 20), height=3)
            label.pack()
            self._items[key].set(f'#{key}\nNumber of votes: 0')

    def _update_label(self, data):
        hashtag, result = data

        total = self._manager.hashtags.get(hashtag.name).total

        self._items[hashtag.name].set(f'#{hashtag.name}\nNumber of votes:{total}')

    def _fetch_data(self):
        self._runner.exec(execute_request, self._manager.hashtags)

    def _on_error(self, error_message):
        raise Exception(error_message)

    def _on_success(self, data):
        hashtag, _ = data
        self._manager.update(data)
        self._update_label(data)

    def _on_complete(self):
        pass


def start_app(args):
    root = Tk()

    app = Application(hashtags=args.hashtags, master=root)
    app.master.title("Twittervotes123456789")
    app.master.geometry("400x700+100+100")
    app.mainloop()


def main():
    args = parse_commandlines_args
    start_app(args)


if __name__ == '__main__':
    main()
