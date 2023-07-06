from easydict import EasyDict

# ==============================================================
# begin of the most frequently changed config specified by the user
# ==============================================================
board_size = 6
collector_env_num = 8
n_episode = 8
evaluator_env_num = 5
update_per_collect = 50
batch_size = 256
max_env_step = int(10e6)
prob_random_action_in_bot = 1

if board_size == 19:
    num_simulations = 800
elif board_size == 9:
    num_simulations = 180
elif board_size == 6:
    num_simulations = 80

# board_size = 6
# collector_env_num = 1
# n_episode = 1
# evaluator_env_num = 1
# num_simulations = 2
# update_per_collect = 2
# batch_size = 2
# max_env_step = int(5e5)
# prob_random_action_in_bot = 0.
# ==============================================================
# end of the most frequently changed config specified by the user
# ==============================================================
gomoku_alphazero_config = dict(
    exp_name=
    f'data_az_ptree/gomoku_alphazero_bot-mode_rand{prob_random_action_in_bot}_ns{num_simulations}_upc{update_per_collect}_seed0',
    env=dict(
        board_size=board_size,
        komi=7.5,
        katago_checkpoint_path="/Users/puyuan/code/KataGo/kata1-b18c384nbt-s6582191360-d3422816034/model.ckpt",
        battle_mode='play_with_bot_mode',
        bot_action_type='v0',
        prob_random_action_in_bot=prob_random_action_in_bot,
        channel_last=True,
        collector_env_num=collector_env_num,
        evaluator_env_num=evaluator_env_num,
        n_evaluator_episode=evaluator_env_num,
        manager=dict(shared_memory=False, ),
    ),
    policy=dict(
        torch_compile=False,
        tensor_float_32=False,
        model=dict(
            observation_shape=(board_size, board_size, 17),
            action_space_size=int(1 * board_size * board_size + 1),
            num_res_blocks=1,
            num_channels=64,
        ),
        cuda=True,
        board_size=board_size,
        update_per_collect=update_per_collect,
        batch_size=batch_size,
        optim_type='AdamW',
        lr_piecewise_constant_decay=False,
        learning_rate=0.003,
        grad_clip_value=10,
        value_weight=1.0,
        entropy_weight=0.0,
        n_episode=n_episode,
        eval_freq=int(2e3),
        replay_buffer_size=int(1e6),
        mcts=dict(num_simulations=num_simulations),
        collector_env_num=collector_env_num,
        evaluator_env_num=evaluator_env_num,
    ),
)

gomoku_alphazero_config = EasyDict(gomoku_alphazero_config)
main_config = gomoku_alphazero_config

gomoku_alphazero_create_config = dict(
    env=dict(
        type='gomoku',
        import_names=['zoo.board_games.gomoku.envs.gomoku_env'],
    ),
    env_manager=dict(type='subprocess'),
    policy=dict(
        type='alphazero',
        import_names=['lzero.policy.alphazero'],
    ),
    collector=dict(
        type='episode_alphazero',
        get_train_sample=False,
        import_names=['lzero.worker.alphazero_collector'],
    ),
    evaluator=dict(
        type='alphazero',
        import_names=['lzero.worker.alphazero_evaluator'],
    )
)
gomoku_alphazero_create_config = EasyDict(gomoku_alphazero_create_config)
create_config = gomoku_alphazero_create_config

if __name__ == '__main__':
    if main_config.policy.tensor_float_32:
        import torch

        # The flag below controls whether to allow TF32 on matmul. This flag defaults to False
        # in PyTorch 1.12 and later.
        torch.backends.cuda.matmul.allow_tf32 = True
        # The flag below controls whether to allow TF32 on cuDNN. This flag defaults to True.
        torch.backends.cudnn.allow_tf32 = True

    from lzero.entry import train_alphazero
    train_alphazero([main_config, create_config], seed=0, max_env_step=max_env_step)
