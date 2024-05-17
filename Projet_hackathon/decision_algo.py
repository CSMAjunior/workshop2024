def decision_algo(game, current_state):
    best_reward = 1e5
    best_rotation = 0
    best_translation = 0
    go = True
    # for all rotation states of the current block
    for r in range(current_state.block.rot):
        possible_action = current_state.list_actions[r]
        # loop over all action for rot r
        for t in possible_action:
            # retreive possible actions for current block b
            action = action_gene(t,r)
            new_state, game_over = game.step(current_state,action)
            if not game_over:
                ### CHANGER ICI LA FONCTION DE RECOMPENSE
                rew = get_reward_mean_line(current_state,new_state)
                if rew < best_reward:
                    best_rotation = r
                    best_translation = t
                    best_reward = rew
                    go = game_over
            
                
    return action_gene(best_translation,best_rotation),go
