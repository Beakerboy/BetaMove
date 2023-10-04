import copy
import heapq
import numpy as np
from typing import TypeVar, Type
from beta_move.beta_move import BetaMove
from beta_move.climb import Climb
from beta_move.moonboard import Moonboard


T = TypeVar('T', bound='BetaGenerator')


class BetaGenerator:

    def __init__(self: T) -> None
    
    @classmethod
    def create_movement(cls: Type[T], climb: Climb) -> BetaMove:
        board = Moonboard()
        beta = BetaMove(board, climb)
        x_vectors = beta.match_hold_features(climb)
        beta.allHolds = x_vectors.T
        beta.totalNumOfHold = np.size(x_vectors.T, axis=0)
        beta.holdsNotUsed = list(range(beta.totalNumOfHold))
        beta1 = copy.deepcopy(beta)
        status = [beta, beta1]
        status[0].add_start_holds(False)
        status[1].add_start_holds(True)
        total_run = status[0].totalNumOfHold - 1

        for i in range(total_run):
            status = BetaGenerator.add_new_beta(status, False)
            final_score = []
            for j in status:
                final_score.append(j.overall_success_rate())
                iter = range(len(final_score))
                key_func = final_score.__getitem__
                largest_index = heapq.nlargest(4, iter, key=key_func)
                comp1 = status[largest_index[0]].isFinished
                if comp1 and status[largest_index[1]].isFinished:
                    break
        final_score = []
        for j in status:
            final_score.append(j.overall_success_rate())
        iter = range(len(final_score))
        key_func = final_score.__getitem__
        largest_index = heapq.nlargest(1, iter, key=key_func)
        return status[largest_index[0]]

    @classmethod
    def add_new_beta(cls: Type[T],
                     status: list,
                     print_out: bool = True
                     ) -> list:
        """
        Add one move to expand the candidate list and pick the largest 8
        """
        tempstatus = []
        for beta_pre in status:
            distance_scores = []
            hyperparameter = [1, 1]
            for next_hold_order in beta_pre.holdsNotUsed:
                original_com = np.array(beta_pre.get_current_com())
                hyper_0 = hyperparameter[0]
                success_rate = beta_pre.last_move_success_rate_by_hold()
                dynamic_threshold = hyper_0 * success_rate
                final_coor = beta_pre.get_xy_from_order(next_hold_order)
                final_xy = np.array(final_coor)
                distance = np.linalg.norm(original_com - final_xy)
                # evaluate success rate simply consider the distance
                # (not consider left and right hand)
                success = beta_pre.success_rate_by_distance(
                    distance,
                    dynamic_threshold
                )
                distance_scores.append(success)
            # Find the first and second smallest distance in the distance_score
            num = min(8, len(distance_scores))
            iter = range(len(distance_scores))
            key_name = distance_scores.__getitem__
            largest_index = heapq.nlargest(num, iter, key=key_name)

            good_hold_index = [beta_pre.holdsNotUsed[i] for i in largest_index]
            added = False
            for possible_hold in good_hold_index:
                for op in ["RH", "LH"]:
                    if not beta_pre.isFinished:
                        tempstatus.append(copy.deepcopy(beta_pre))
                        tempstatus[-1].add_next_hand(possible_hold, op)
                    elif not added:
                        tempstatus.append(copy.deepcopy(beta_pre))
                        added = True

        # trim tempstatus to pick the largest 8
        final_score = []
        for i in tempstatus:
            final_score.append(i.overall_success_rate())
        iter = range(len(final_score))
        largest_index = heapq.nlargest(8, iter, key=final_score.__getitem__)
        return [tempstatus[i] for i in largest_index]
