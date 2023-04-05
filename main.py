from kivy.core.text import LabelBase
from kivymd.app import MDApp
from kivy.lang.builder import Builder
from TicTacToeBrain import TicTacToePlayer

P1 = "X"
P2 = "O"
P1_SCORE = 0
P2_SCORE = 0

LabelBase.register(name='Arilon', fn_regular='fonts/arilon.ttf')


class TicTacToeGame(MDApp):

    def __init__(self):
        super().__init__()
        self.current_player = P1
        self.p1_score = 0
        self.p2_score = 0
        self.game = None
        self.game_type = None

    def build(self):
        self.theme_cls.primary_palette = 'BlueGray'
        self.theme_cls.primary_hue = '500'
        self.theme_cls.theme_style = 'Light'
        return Builder.load_file('TicTacToeGameLayout.kv')

    def on_tt_press(self, instance) -> None:
        """ On Board Click triggers the game turns """
        if self.game_type == 'multi_player':
            self.multi_player_manager(instance=instance)
        if self.game_type == "single_player":
            self.single_player_manager(instance=instance)

    def multi_player_manager(self, instance) -> None:
        """ Switch between players and place/evaluate their plays """
        pos = int(instance.name[-1])
        player_label = instance.parent.parent.parent.ids['player']
        self.mark_the_board(instance=instance)
        self.game.play_turn(pos=pos, player=self.current_player)

        if self.keep_playing(instance=instance):
            self.switch_player()
            player_label.text = f"{self.current_player} Player Turn"

    def single_player_manager(self, instance) -> None:
        """ Switch between player and AI and place/evaluate their plays """
        pos = int(instance.name[-1])
        player_label = instance.parent.parent.parent.ids['player']

        if self.current_player == "X":
            self.mark_the_board(instance=instance)
            self.game.play_turn(pos=pos, player=self.current_player)

            if self.keep_playing(instance=instance):
                self.switch_player()
                player_label.text = f"{self.current_player} Player Turn"

        if self.current_player == "O":
            ai_move = self.game.play_ai_turn(player=self.current_player)
            btn_name = f'btn{ai_move}'
            ai_board = instance.parent.parent.parent.ids[btn_name]
            self.mark_the_board(instance=ai_board)

            if self.keep_playing(instance=instance):
                self.switch_player()
                player_label.text = f"{self.current_player} Player Turn"

    def keep_playing(self, instance) -> bool:
        """ Check winning or full board conditions after each player turn """
        if self.game.is_winner():
            self.stop_game(instance=instance, winner=True)
            return False
        elif self.game.is_board_full():
            self.stop_game(instance=instance, winner=False)
            return False
        return True

    def mark_the_board(self, instance) -> None:
        """ Place the current player play on the board and disables it. """
        instance.text = self.current_player.upper()
        instance.disabled = True
        instance.disabled_background_color = '#ffffff'
        if self.current_player == "X":
            instance.disabled_color = "#7788ee"
        else:
            instance.disabled_color = "ee8877"

    def switch_player(self) -> None:
        """ Simple switch between players """
        if self.current_player == "X":
            self.current_player = "O"
        else:
            self.current_player = "X"

    def start_game(self, instance, game_mode: str) -> None:
        """ Starts the game, hides the buttons and enables the board. Plays AI's turn if needed. """
        self.game_type = game_mode
        self.hide_buttons(instance=instance)

        player_label = instance.parent.ids['player']
        player_label.text = f"{self.current_player} Player Turn"

        board = instance.parent.ids['game_board'].children
        for each in board:
            each.disabled = False
            each.text = ''
            each.background_color = '#E4F6F8'

        self.game = TicTacToePlayer()

        if self.current_player == "O" and self.game_type == "single_player":
            button = instance.parent.ids['btn1']
            self.on_tt_press(instance=button)

    def stop_game(self, instance, winner: bool) -> None:
        """ Stops the game on Win/Tie. Disables the board. Assigns points to the winner. """
        self.show_buttons(instance=instance)

        player_label = instance.parent.parent.parent.ids['player']

        if winner:
            player_label.text = f"{self.current_player} Player Won!"
            if self.current_player == "X":
                self.p1_score += 1
                instance.parent.parent.parent.ids['score_1'].text = f"Player X: {self.p1_score}"
            else:
                self.p2_score += 1
                instance.parent.parent.parent.ids['score_2'].text = f"Player O: {self.p2_score}"

        else:
            player_label.text = f"It's a Tie"

        board = instance.parent.parent.parent.ids['game_board'].children
        for each in board:
            each.disabled = True
            each.background_color = "#e4f8f0"

    def show_buttons(self, instance) -> None:
        """ Shows buttons on finished game/reset """
        start_game_multi_btn = instance.parent.parent.parent.ids['start_game_multi']
        start_game_single_btn = instance.parent.parent.parent.ids['start_game_single']

        if self.game_type == 'single_player':
            start_game_single_btn.text = "Another try?"
            start_game_single_btn.disabled = False
            start_game_single_btn.opacity = 1
        elif self.game_type == 'multi_player':
            start_game_multi_btn.text = "Another game?"
            start_game_multi_btn.disabled = False
            start_game_multi_btn.opacity = 1
        else:
            start_game_single_btn.text = "Play with an AI"
            start_game_single_btn.disabled = False
            start_game_single_btn.opacity = 1

            start_game_multi_btn.text = "Play with a Friend"
            start_game_multi_btn.disabled = False
            start_game_multi_btn.opacity = 1

    @staticmethod
    def hide_buttons(instance) -> None:
        """ Hides buttons on new game start """
        single_player_btn = instance.parent.ids['start_game_single']
        single_player_btn.disabled = True
        single_player_btn.opacity = 0

        multi_player_btn = instance.parent.ids['start_game_multi']
        multi_player_btn.disabled = True
        multi_player_btn.opacity = 0

    def reset(self, instance) -> None:
        """ Reset the game to initial state. """
        start_game_multi_btn = instance.parent.ids['start_game_multi']
        start_game_single_btn = instance.parent.ids['start_game_single']

        start_game_single_btn.text = "Play with an AI"
        start_game_single_btn.disabled = False
        start_game_single_btn.opacity = 1

        start_game_multi_btn.text = "Play with a Friend"
        start_game_multi_btn.disabled = False
        start_game_multi_btn.opacity = 1

        board = instance.parent.ids['game_board'].children
        for each in board:
            each.disabled = True
            each.text = ""
            each.background_color = "#FFFFFF"

        self.p1_score = 0
        self.p2_score = 0
        instance.parent.ids['score_1'].text = f"Player X: {self.p1_score}"
        instance.parent.ids['score_2'].text = f"Player O: {self.p2_score}"


if __name__ == "__main__":
    TicTacToeGame().run()
