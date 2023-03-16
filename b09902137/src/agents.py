from game.players import BasePokerPlayer
import agents.prob as prob

class CallPlayer(
    BasePokerPlayer
):  # Do not forget to make parent class as "BasePokerPlayer"

    #  we define the logic to make an action through this method. (so this method would be the core of your AI)
    def declare_action(self, valid_actions, hole_card, round_state):
        # valid_actions format => [raise_action_info, call_action_info, fold_action_info]
        remain = (20-round_state["round_count"])*10
        raise_info = valid_actions[2]
        raise_action, raise_amt = raise_info["action"], raise_info["amount"]
        call_info = valid_actions[1]
        call_action, call_amt = call_info["action"], call_info["amount"]
        fold_info = valid_actions[0]
        fold_action, fold_amt = fold_info["action"], fold_info["amount"]
        if (raise_amt["max"]-1000 > remain):
            return fold_action, fold_amt
        com = round_state["community_card"]
        p = prob.evl_rate(hole_card, com) 
        #   define threshold
        fold_thres = 0.15 ; call_thres = 0.65
        if (len(com) == 0):
            if (p > 0.35):
                raise_amt = p*0.1*raise_amt["max"]
                return raise_action, raise_amt
            else:
                return call_action, call_amt
        else:
            if (p < fold_thres and call_amt < 50):
                return call_action, call_amt
            elif (p < fold_thres and call_amt > 50):
                return fold_action, fold_amt
            elif (p < call_thres and call_amt > 300):
                return fold_action, fold_amt
            elif (p < call_thres and call_amt < 300):
                return call_action, call_amt
            elif (p >= call_thres):
                return raise_action, p*raise_amt["max"]
            else:
                return fold_action, fold_amt
        # call_action_info = valid_actions[1]
        # action, amount = call_action_info["action"], call_action_info["amount"]
        # return action, amount  # action returned here is sent to the poker engine

    def receive_game_start_message(self, game_info):
        pass

    def receive_round_start_message(self, round_count, hole_card, seats):
        pass

    def receive_street_start_message(self, street, round_state):
        pass

    def receive_game_update_message(self, action, round_state):
        pass

    def receive_round_result_message(self, winners, hand_info, round_state):
        pass


def setup_ai():
    return CallPlayer()
