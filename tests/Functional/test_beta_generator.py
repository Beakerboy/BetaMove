from beta_move.beta_generator import BetaGenerator


create_movement_data = [
    [
        "342797",
        [
            [0, 0, 1, 3, 4, 5, 7, 8],
            ['LH', 'RH', 'LH', 'RH', 'LH', 'RH', 'LH', 'RH'],
            98.503968934466
        ]
    ],
    [
        "20149",
        [
            [0, 1, 2, 4, 5, 6, 7],
            ['LH', 'RH', 'LH', 'RH', 'LH', 'LH', 'RH'],
            6.559208130702623
        ]
    ]
]


@pytest.mark.parametrize("problem_id, expected", create_movement_data)
def test_create_movement(problem_id: str, expected: list) -> None:
    app = BetaGenerator()
    f = open('tests/pickle_data/moonGen_scrape_2016_final.pkl', 'rb')
    all_climbs = pickle.load(f)
    climb = Climb.from_old_json(problem_id, all_climbs[problem_id])
    result = app.create_movement(climb)
    assert result.handSequence == expected[0]
    assert result.handOperator == expected[1]
    assert result.overall_success_rate() == expected[2]
