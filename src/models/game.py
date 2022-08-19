from peewee import *

import config


class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):
    class Meta:
        database = config.game_env.db


class AchievementCategories(BaseModel):
    created_at = DateTimeField()
    description = TextField(null=True)
    name = CharField()
    open_at = DateTimeField()
    parent_category_id = BigIntegerField(index=True, null=True)
    priority = IntegerField(constraints=[SQL("DEFAULT 0")])
    updated_at = DateTimeField()

    class Meta:
        table_name = 'achievement_categories'
        indexes = (
            (('open_at', 'priority'), False),
        )


class Achievements(BaseModel):
    achievement_category_id = BigIntegerField(index=True)
    created_at = DateTimeField()
    description = TextField()
    frame_image_name = CharField()
    link_to = CharField(null=True)
    name = CharField()
    open_at = DateTimeField()
    priority = IntegerField(constraints=[SQL("DEFAULT 0")])
    rarity = IntegerField(constraints=[SQL("DEFAULT 0")])
    updated_at = DateTimeField()

    class Meta:
        table_name = 'achievements'
        indexes = (
            (('open_at', 'priority'), False),
        )


class ActCureSchedules(BaseModel):
    created_at = DateTimeField()
    end_at = DateTimeField()
    seconds_per_cure_one_act = IntegerField()
    start_at = DateTimeField()
    updated_at = DateTimeField()

    class Meta:
        table_name = 'act_cure_schedules'


class ActItems(BaseModel):
    created_at = DateTimeField()
    description = CharField()
    name = CharField()
    rarity = IntegerField(constraints=[SQL("DEFAULT 0")])
    recover_value = IntegerField(constraints=[SQL("DEFAULT 0")])
    selling_exchange_point = IntegerField(constraints=[SQL("DEFAULT 0")])
    updated_at = DateTimeField()

    class Meta:
        table_name = 'act_items'


class ActiveSkillSets(BaseModel):
    bgm_id = IntegerField(null=True)
    causality_conditions = TextField(null=True)
    condition_description = TextField()
    costume_special_view_id = BigIntegerField()
    created_at = DateTimeField()
    effect_description = TextField()
    exec_limit = IntegerField(constraints=[SQL("DEFAULT 1")])
    name = CharField()
    special_view_id = IntegerField(null=True)
    turn = IntegerField(constraints=[SQL("DEFAULT 0")])
    ultimate_special_id = IntegerField(null=True)
    updated_at = DateTimeField()

    class Meta:
        table_name = 'active_skill_sets'


class ActiveSkills(BaseModel):
    active_skill_set_id = IntegerField(index=True)
    calc_option = IntegerField(constraints=[SQL("DEFAULT 0")])
    created_at = DateTimeField()
    eff_val1 = IntegerField(constraints=[SQL("DEFAULT 0")])
    eff_val2 = IntegerField(constraints=[SQL("DEFAULT 0")])
    eff_val3 = IntegerField(constraints=[SQL("DEFAULT 0")])
    effect_se_id = IntegerField(null=True)
    efficacy_type = IntegerField(constraints=[SQL("DEFAULT 0")])
    sub_target_type_set_id = IntegerField(null=True)
    target_type = IntegerField(constraints=[SQL("DEFAULT 0")])
    thumb_effect_id = IntegerField(null=True)
    updated_at = DateTimeField()

    class Meta:
        table_name = 'active_skills'


class AreaConditions(BaseModel):
    area_id = IntegerField(index=True)
    comment = CharField()
    conditions = UnknownField(null=True)  # json
    created_at = DateTimeField()
    type = CharField()
    updated_at = DateTimeField()

    class Meta:
        table_name = 'area_conditions'


class AreaIcons(BaseModel):
    created_at = DateTimeField()
    icon_x = IntegerField(null=True)
    icon_y = IntegerField(null=True)
    image = CharField(null=True)
    updated_at = DateTimeField()
    world_id = IntegerField(index=True)

    class Meta:
        table_name = 'area_icons'


class AreaRecommends(BaseModel):
    area_id = IntegerField(index=True)
    created_at = DateTimeField()
    description = CharField()
    priority = IntegerField()
    rank_range_id = IntegerField(index=True)
    updated_at = DateTimeField()

    class Meta:
        table_name = 'area_recommends'


class AreaTabs(BaseModel):
    area_category_ids = UnknownField(null=True)  # json
    created_at = DateTimeField()
    limited = IntegerField(constraints=[SQL("DEFAULT 0")])
    name = CharField(null=True)
    updated_at = DateTimeField()

    class Meta:
        table_name = 'area_tabs'


class Areas(BaseModel):
    all_clear_bonus_stones = IntegerField(null=True)
    announcement_id = IntegerField(index=True, null=True)
    area_icon_id = IntegerField(null=True)
    banner_image_path = CharField(null=True)
    bgm_id = IntegerField(null=True)
    category = IntegerField(null=True)
    created_at = DateTimeField()
    db_story_id = IntegerField(null=True)
    event_image_path = CharField(null=True)
    event_priority = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    first_released_at = DateTimeField(null=True)
    height = IntegerField(null=True)
    is_listbutton_visible = IntegerField()
    is_quest_num_visible = IntegerField(constraints=[SQL("DEFAULT 1")])
    layer0 = CharField(null=True)
    layer1 = CharField(null=True)
    layer2 = CharField(null=True)
    layer3 = CharField(null=True)
    listbutton_image_path = CharField(null=True)
    minibanner_image_path = CharField(null=True)
    name = CharField()
    prev_area_id = IntegerField(index=True, null=True)
    split = IntegerField(null=True)
    type = CharField(null=True)
    updated_at = DateTimeField()
    width = IntegerField(null=True)
    world_id = IntegerField(index=True)

    class Meta:
        table_name = 'areas'


class AwakeningItems(BaseModel):
    created_at = DateTimeField()
    description = CharField()
    event_jumpable = IntegerField(constraints=[SQL("DEFAULT 1")], null=True)
    name = CharField()
    rarity = IntegerField(constraints=[SQL("DEFAULT 0")])
    selling_exchange_point = IntegerField(constraints=[SQL("DEFAULT 0")])
    updated_at = DateTimeField()
    zeni = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'awakening_items'


class BattleParams(BaseModel):
    created_at = DateTimeField()
    idx = IntegerField()
    param_no = IntegerField(index=True)
    updated_at = DateTimeField()
    value = IntegerField()

    class Meta:
        table_name = 'battle_params'


class BgmSchedules(BaseModel):
    bgm_id = IntegerField()
    created_at = DateTimeField()
    end_at = DateTimeField()
    scene_name = CharField()
    start_at = DateTimeField()
    updated_at = DateTimeField()

    class Meta:
        table_name = 'bgm_schedules'


class BoostSchedules(BaseModel):
    created_at = DateTimeField()
    end_at = DateTimeField()
    max_point = IntegerField()
    seconds_per_cure_one_point = IntegerField()
    start_at = DateTimeField()
    updated_at = DateTimeField()

    class Meta:
        table_name = 'boost_schedules'


class BudokaiBoxRankingRewardRanges(BaseModel):
    budokai_box_ranking_id = IntegerField(index=True)
    created_at = DateTimeField()
    end_value = IntegerField()
    start_value = IntegerField()
    updated_at = DateTimeField()

    class Meta:
        table_name = 'budokai_box_ranking_reward_ranges'


class BudokaiBoxRankingRewards(BaseModel):
    budokai_box_ranking_reward_range_id = IntegerField(index=True)
    card_exp_init = IntegerField(constraints=[SQL("DEFAULT 0")])
    created_at = DateTimeField()
    description = CharField()
    gift_description = CharField()
    item_id = IntegerField()
    item_type = CharField()
    quantity = IntegerField(constraints=[SQL("DEFAULT 0")])
    updated_at = DateTimeField()

    class Meta:
        table_name = 'budokai_box_ranking_rewards'


class BudokaiBoxRankings(BaseModel):
    box_max_count = IntegerField(null=True)
    budokai_id = IntegerField(index=True)
    collecting_end_at = DateTimeField()
    created_at = DateTimeField()
    end_at = DateTimeField()
    player_max_count = IntegerField()
    prev_budokai_box_ranking_id = IntegerField(null=True)
    prev_budokai_id = IntegerField(null=True)
    start_at = DateTimeField()
    updated_at = DateTimeField()

    class Meta:
        table_name = 'budokai_box_rankings'


class BudokaiHelpBodies(BaseModel):
    budokai_help_id = IntegerField(index=True, null=True)
    created_at = DateTimeField()
    description = TextField(null=True)
    image_path = CharField(null=True)
    updated_at = DateTimeField()

    class Meta:
        table_name = 'budokai_help_bodies'


class BudokaiHelpCategories(BaseModel):
    created_at = DateTimeField()
    num = IntegerField(null=True)
    title = CharField()
    updated_at = DateTimeField()

    class Meta:
        table_name = 'budokai_help_categories'


class BudokaiHelps(BaseModel):
    budokai_help_category_id = IntegerField()
    created_at = DateTimeField()
    description = TextField(null=True)
    num = IntegerField(null=True)
    title = CharField()
    updated_at = DateTimeField()

    class Meta:
        table_name = 'budokai_helps'


class BudokaiLeagues(BaseModel):
    budokai_id = IntegerField()
    created_at = DateTimeField()
    league = IntegerField()
    name = CharField()
    updated_at = DateTimeField()

    class Meta:
        table_name = 'budokai_leagues'
        indexes = (
            (('budokai_id', 'league'), True),
        )


class BudokaiMissionRewards(BaseModel):
    budokai_mission_id = IntegerField(index=True)
    card_exp_init = IntegerField(constraints=[SQL("DEFAULT 0")])
    created_at = DateTimeField()
    description = CharField()
    gift_description = CharField()
    item_id = IntegerField()
    item_type = CharField()
    quantity = IntegerField(constraints=[SQL("DEFAULT 0")])
    updated_at = DateTimeField()

    class Meta:
        table_name = 'budokai_mission_rewards'


class BudokaiMissions(BaseModel):
    budokai_id = IntegerField()
    created_at = DateTimeField()
    mission_type = IntegerField()
    name = CharField()
    prev_budokai_mission_id = IntegerField(null=True)
    priority = IntegerField()
    target_value = IntegerField(constraints=[SQL("DEFAULT 0")])
    updated_at = DateTimeField()

    class Meta:
        table_name = 'budokai_missions'
        indexes = (
            (('budokai_id', 'mission_type'), False),
        )


class BudokaiMotivationUnlockConditions(BaseModel):
    budokai_motivation_id = IntegerField(index=True)
    conditions = UnknownField(null=True)  # json
    created_at = DateTimeField()
    description = CharField(null=True)
    type = CharField(null=True)
    updated_at = DateTimeField()

    class Meta:
        table_name = 'budokai_motivation_unlock_conditions'


class BudokaiMotivations(BaseModel):
    additional_atk_percent = IntegerField(constraints=[SQL("DEFAULT 0")])
    additional_def_percent = IntegerField(constraints=[SQL("DEFAULT 0")])
    additional_hp_percent = IntegerField(constraints=[SQL("DEFAULT 0")])
    additional_point_percent = IntegerField(constraints=[SQL("DEFAULT 0")])
    announcer_description = CharField(null=True)
    budokai_id = IntegerField(index=True)
    created_at = DateTimeField()
    max_atk_percent = IntegerField(constraints=[SQL("DEFAULT 0")])
    max_def_percent = IntegerField(constraints=[SQL("DEFAULT 0")])
    max_hp_percent = IntegerField(constraints=[SQL("DEFAULT 0")])
    player_description = CharField()
    priority = IntegerField(constraints=[SQL("DEFAULT 0")])
    updated_at = DateTimeField()

    class Meta:
        table_name = 'budokai_motivations'


class BudokaiOpponentAttackWeightLines(BaseModel):
    ball_count = IntegerField()
    budokai_opponent_attack_weight_id = IntegerField()
    rate = IntegerField()

    class Meta:
        table_name = 'budokai_opponent_attack_weight_lines'


class BudokaiOpponentAttackWeights(BaseModel):
    budokai_id = IntegerField()
    created_at = DateTimeField()
    round = IntegerField()
    updated_at = DateTimeField()

    class Meta:
        table_name = 'budokai_opponent_attack_weights'
        indexes = (
            (('budokai_id', 'round'), True),
        )


class BudokaiProgressSelifs(BaseModel):
    budokai_id = IntegerField()
    description = TextField(null=True)
    image_path = CharField(null=True)
    round = IntegerField()

    class Meta:
        table_name = 'budokai_progress_selifs'
        indexes = (
            (('budokai_id', 'round'), True),
        )


class BudokaiRankingGiftSets(BaseModel):
    budokai_id = IntegerField()
    created_at = DateTimeField()
    order = IntegerField()
    ranking = CharField()
    updated_at = DateTimeField()

    class Meta:
        table_name = 'budokai_ranking_gift_sets'
        indexes = (
            (('budokai_id', 'order'), True),
        )


class BudokaiRankingGifts(BaseModel):
    budokai_ranking_gift_set_id = IntegerField(index=True)
    card_exp_init = IntegerField(constraints=[SQL("DEFAULT 0")])
    created_at = DateTimeField()
    description = CharField(null=True)
    item_id = IntegerField()
    item_type = CharField()
    quantity = IntegerField()
    updated_at = DateTimeField()

    class Meta:
        table_name = 'budokai_ranking_gifts'


class BudokaiRanks(BaseModel):
    bonus = FloatField(constraints=[SQL("DEFAULT 1.0")])
    budokai_id = IntegerField()
    budokai_league_id = IntegerField()
    created_at = DateTimeField()
    name = CharField()
    point = IntegerField()
    rank = IntegerField()
    updated_at = DateTimeField()

    class Meta:
        table_name = 'budokai_ranks'
        indexes = (
            (('budokai_id', 'rank'), True),
        )


class Budokais(BaseModel):
    banner_image_path = CharField()
    collecting_end_at = DateTimeField()
    created_at = DateTimeField()
    description = TextField()
    description_script_id = IntegerField(constraints=[SQL("DEFAULT 0")])
    enable_battle_auto = IntegerField(constraints=[SQL("DEFAULT 0")])
    end_at = DateTimeField()
    entry_script_id = IntegerField(constraints=[SQL("DEFAULT 0")])
    home_banner_image_path = CharField(null=True)
    listbutton_image_path = CharField(null=True)
    mission_reward_image_path = CharField()
    name = CharField()
    result_end_at = DateTimeField()
    start_at = DateTimeField()
    updated_at = DateTimeField()

    class Meta:
        table_name = 'budokais'


class CardActiveSkills(BaseModel):
    active_skill_set_id = IntegerField()
    card_id = IntegerField(unique=True)
    created_at = DateTimeField()
    updated_at = DateTimeField()

    class Meta:
        table_name = 'card_active_skills'


class CardAwakeningRoutes(BaseModel):
    awaked_card_id = IntegerField(index=True, null=True)
    card_awakening_set_id = IntegerField(index=True)
    card_id = IntegerField(index=True)
    created_at = DateTimeField()
    description = TextField(null=True)
    num = IntegerField(null=True)
    open_at = DateTimeField(constraints=[SQL("DEFAULT '2010-04-01 00:00:00'")], null=True)
    optimal_awakening_step = IntegerField(null=True)
    priority = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    type = CharField()
    updated_at = DateTimeField()

    class Meta:
        table_name = 'card_awakening_routes'


class CardAwakeningSets(BaseModel):
    created_at = DateTimeField()
    description = CharField(null=True)
    name = CharField(null=True)
    updated_at = DateTimeField()

    class Meta:
        table_name = 'card_awakening_sets'


class CardAwakenings(BaseModel):
    awakening_item_id = IntegerField()
    card_awakening_set_id = IntegerField(index=True, null=True)
    created_at = DateTimeField()
    num = IntegerField(constraints=[SQL("DEFAULT 0")])
    quantity = IntegerField(constraints=[SQL("DEFAULT 0")])
    updated_at = DateTimeField()

    class Meta:
        table_name = 'card_awakenings'


class CardCardCategories(BaseModel):
    card_category_id = BigIntegerField(index=True)
    card_id = BigIntegerField()
    created_at = DateTimeField()
    num = IntegerField()
    updated_at = DateTimeField()

    class Meta:
        table_name = 'card_card_categories'
        indexes = (
            (('card_id', 'card_category_id'), True),
            (('card_id', 'num'), True),
        )


class CardCategories(BaseModel):
    created_at = DateTimeField()
    kana = CharField(null=True)
    name = CharField()
    open_at = DateTimeField()
    priority = IntegerField(constraints=[SQL("DEFAULT 0")])
    updated_at = DateTimeField()

    class Meta:
        table_name = 'card_categories'


class CardCostumeConditions(BaseModel):
    card_costume_id = BigIntegerField()
    card_id = BigIntegerField(index=True)
    conditions = UnknownField()  # json
    counter_script_no = IntegerField(null=True)
    created_at = DateTimeField()
    description = TextField()
    revive_effect_pack_id = IntegerField(null=True)
    updated_at = DateTimeField()

    class Meta:
        table_name = 'card_costume_conditions'


class CardCostumes(BaseModel):
    card_id = BigIntegerField()
    created_at = DateTimeField()
    updated_at = DateTimeField()

    class Meta:
        table_name = 'card_costumes'


class CardDecorations(BaseModel):
    card_id = BigIntegerField(index=True)
    created_at = DateTimeField()
    priority = IntegerField(constraints=[SQL("DEFAULT 0")])
    updated_at = DateTimeField()

    class Meta:
        table_name = 'card_decorations'


class CardExps(BaseModel):
    created_at = DateTimeField()
    exp_total = IntegerField(constraints=[SQL("DEFAULT 0")])
    exp_type = IntegerField(constraints=[SQL("DEFAULT 0")])
    lv = IntegerField(constraints=[SQL("DEFAULT 0")])
    updated_at = DateTimeField()

    class Meta:
        table_name = 'card_exps'
        indexes = (
            (('exp_total', 'lv', 'exp_type'), True),
            (('exp_type', 'exp_total'), True),
            (('lv', 'exp_type'), True),
        )


class CardGrowths(BaseModel):
    coef = FloatField()
    created_at = DateTimeField()
    grow_type = IntegerField()
    lv = IntegerField()
    updated_at = DateTimeField()

    class Meta:
        table_name = 'card_growths'
        indexes = (
            (('grow_type', 'lv'), True),
        )


class CardMotions(BaseModel):
    card_id = IntegerField()
    category = IntegerField()
    created_at = DateTimeField()
    filename = CharField(null=True)
    updated_at = DateTimeField()

    class Meta:
        table_name = 'card_motions'
        indexes = (
            (('card_id', 'category', 'filename'), True),
        )


class CardSpecials(BaseModel):
    bonus_view_id1 = IntegerField(constraints=[SQL("DEFAULT 0")])
    bonus_view_id2 = IntegerField(constraints=[SQL("DEFAULT 0")])
    card_costume_condition_id = BigIntegerField()
    card_id = IntegerField(index=True)
    causality_conditions = TextField(null=True)
    created_at = DateTimeField()
    eball_num_start = IntegerField(constraints=[SQL("DEFAULT 12")])
    lv_start = IntegerField(constraints=[SQL("DEFAULT 0")])
    priority = IntegerField(null=True)
    special_asset_id = BigIntegerField(null=True)
    special_bonus_id1 = IntegerField(constraints=[SQL("DEFAULT 0")])
    special_bonus_id2 = IntegerField(constraints=[SQL("DEFAULT 0")])
    special_bonus_lv1 = IntegerField(constraints=[SQL("DEFAULT 0")])
    special_bonus_lv2 = IntegerField(constraints=[SQL("DEFAULT 0")])
    special_set_id = IntegerField()
    style = CharField()
    updated_at = DateTimeField()
    view_id = IntegerField()

    class Meta:
        table_name = 'card_specials'


class CardStickerDecorationRelations(BaseModel):
    card_decoration_id = BigIntegerField()
    card_sticker_item_id = BigIntegerField()
    created_at = DateTimeField()
    open_at = DateTimeField()
    updated_at = DateTimeField()

    class Meta:
        table_name = 'card_sticker_decoration_relations'
        indexes = (
            (('card_sticker_item_id', 'card_decoration_id'), True),
        )


class CardStickerItems(BaseModel):
    created_at = DateTimeField()
    description = CharField()
    name = CharField()
    priority = IntegerField(constraints=[SQL("DEFAULT 0")])
    rarity = IntegerField(constraints=[SQL("DEFAULT 0")])
    updated_at = DateTimeField()

    class Meta:
        table_name = 'card_sticker_items'


class CardTrainingFieldExpUpProbs(BaseModel):
    created_at = DateTimeField()
    effect = FloatField(constraints=[SQL("DEFAULT 0.0")])
    key = CharField(unique=True)
    success_prob_percent = FloatField(constraints=[SQL("DEFAULT 0.0")])
    updated_at = DateTimeField()

    class Meta:
        table_name = 'card_training_field_exp_up_probs'


class CardTrainingSkillLvUpProbs(BaseModel):
    lr = IntegerField(constraints=[SQL("DEFAULT 0")])
    n = IntegerField(constraints=[SQL("DEFAULT 0")])
    r = IntegerField(constraints=[SQL("DEFAULT 0")])
    rarity = CharField(unique=True)
    sr = IntegerField(constraints=[SQL("DEFAULT 0")])
    ssr = IntegerField(constraints=[SQL("DEFAULT 0")])
    ur = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'card_training_skill_lv_up_probs'


class CardTrainingSkillLvs(BaseModel):
    card_id = IntegerField(index=True)
    condition = IntegerField(constraints=[SQL("DEFAULT 0")])
    created_at = DateTimeField()
    probability = IntegerField(constraints=[SQL("DEFAULT 100")])
    skill_lv = IntegerField(constraints=[SQL("DEFAULT 1")])
    updated_at = DateTimeField()

    class Meta:
        table_name = 'card_training_skill_lvs'


class CardUniqueInfoSetRelations(BaseModel):
    card_unique_info_id = IntegerField()
    card_unique_info_set_id = BigIntegerField()
    created_at = DateTimeField()
    updated_at = DateTimeField()

    class Meta:
        table_name = 'card_unique_info_set_relations'
        indexes = (
            (('card_unique_info_set_id', 'card_unique_info_id'), True),
        )


class CardUniqueInfos(BaseModel):
    created_at = DateTimeField()
    kana = CharField(null=True)
    name = CharField()
    updated_at = DateTimeField()

    class Meta:
        table_name = 'card_unique_infos'


class Cards(BaseModel):
    atk_init = IntegerField(constraints=[SQL("DEFAULT 0")])
    atk_max = IntegerField(constraints=[SQL("DEFAULT 0")])
    aura_id = IntegerField(null=True)
    aura_offset_x = IntegerField(null=True)
    aura_offset_y = IntegerField(null=True)
    aura_scale = FloatField(null=True)
    awakening_element_type = IntegerField(null=True)
    awakening_number = IntegerField(null=True)
    bg_effect_id = IntegerField(null=True)
    card_unique_info_id = IntegerField()
    character_id = IntegerField()
    collectable_type = IntegerField(null=True)
    cost = IntegerField(constraints=[SQL("DEFAULT 0")])
    created_at = DateTimeField()
    def_init = IntegerField(constraints=[SQL("DEFAULT 0")])
    def_max = IntegerField(constraints=[SQL("DEFAULT 0")])
    eball_mod_max = IntegerField()
    eball_mod_max_num = IntegerField()
    eball_mod_mid = IntegerField(constraints=[SQL("DEFAULT 0")])
    eball_mod_mid_num = IntegerField(constraints=[SQL("DEFAULT 0")])
    eball_mod_min = IntegerField()
    eball_mod_num100 = IntegerField()
    element = IntegerField(constraints=[SQL("DEFAULT 0")])
    exp_type = IntegerField(constraints=[SQL("DEFAULT 0")])
    face_x = IntegerField(constraints=[SQL("DEFAULT 0")])
    face_y = IntegerField(constraints=[SQL("DEFAULT 0")])
    grow_type = IntegerField(constraints=[SQL("DEFAULT 0")])
    hp_init = IntegerField(constraints=[SQL("DEFAULT 0")])
    hp_max = IntegerField(constraints=[SQL("DEFAULT 0")])
    is_aura_front = IntegerField(constraints=[SQL("DEFAULT 0")])
    is_selling_only = IntegerField(constraints=[SQL("DEFAULT 0")])
    leader_skill_set_id = BigIntegerField(index=True, null=True)
    link_skill1_id = IntegerField(null=True)
    link_skill2_id = IntegerField(null=True)
    link_skill3_id = IntegerField(null=True)
    link_skill4_id = IntegerField(null=True)
    link_skill5_id = IntegerField(null=True)
    link_skill6_id = IntegerField(null=True)
    link_skill7_id = IntegerField(null=True)
    lv_max = IntegerField(constraints=[SQL("DEFAULT 0")])
    max_level_reward_id = IntegerField(null=True)
    max_level_reward_type = CharField(null=True)
    name = CharField()
    open_at = DateTimeField()
    optimal_awakening_grow_type = IntegerField(null=True)
    passive_skill_set_id = IntegerField(null=True)
    potential_board_id = IntegerField(null=True)
    price = IntegerField(constraints=[SQL("DEFAULT 0")])
    rarity = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    resource_id = IntegerField(null=True)
    selling_exchange_point = IntegerField(constraints=[SQL("DEFAULT 0")])
    skill_lv_max = IntegerField(constraints=[SQL("DEFAULT 0")])
    special_motion = IntegerField(constraints=[SQL("DEFAULT 1")])
    training_exp = IntegerField(constraints=[SQL("DEFAULT 0")])
    updated_at = DateTimeField()

    class Meta:
        table_name = 'cards'


class ChainBattleHelpBodies(BaseModel):
    chain_battle_help_id = BigIntegerField(index=True)
    created_at = DateTimeField()
    description = TextField(null=True)
    image_path = CharField(null=True)
    updated_at = DateTimeField()

    class Meta:
        table_name = 'chain_battle_help_bodies'


class ChainBattleHelpCategories(BaseModel):
    created_at = DateTimeField()
    num = IntegerField(null=True)
    title = CharField()
    updated_at = DateTimeField()

    class Meta:
        table_name = 'chain_battle_help_categories'


class ChainBattleHelps(BaseModel):
    chain_battle_help_category_id = BigIntegerField(index=True)
    created_at = DateTimeField()
    description = CharField(null=True)
    num = IntegerField(null=True)
    title = CharField()
    updated_at = DateTimeField()

    class Meta:
        table_name = 'chain_battle_helps'


class ChainBattleMissionPeriods(BaseModel):
    chain_battle_mission_id = IntegerField(index=True)
    created_at = DateTimeField()
    type = CharField(null=True)
    updated_at = DateTimeField()

    class Meta:
        table_name = 'chain_battle_mission_periods'


class ChainBattleMissionRewards(BaseModel):
    card_exp_init = IntegerField(constraints=[SQL("DEFAULT 0")])
    chain_battle_mission_id = BigIntegerField(index=True)
    created_at = DateTimeField()
    description = CharField()
    gift_description = CharField()
    item_id = BigIntegerField()
    item_type = CharField()
    quantity = IntegerField()
    updated_at = DateTimeField()

    class Meta:
        table_name = 'chain_battle_mission_rewards'


class ChainBattleMissions(BaseModel):
    chain_battle_id = BigIntegerField(index=True)
    conditions = UnknownField(null=True)  # json
    created_at = DateTimeField()
    name = CharField()
    priority = IntegerField()
    target_value = BigIntegerField()
    type = CharField()
    updated_at = DateTimeField()

    class Meta:
        table_name = 'chain_battle_missions'


class ChainBattleRankingGiftSets(BaseModel):
    chain_battle_id = BigIntegerField(index=True)
    created_at = DateTimeField()
    percentile = IntegerField()
    updated_at = DateTimeField()

    class Meta:
        table_name = 'chain_battle_ranking_gift_sets'


class ChainBattleRankingGifts(BaseModel):
    card_exp_init = IntegerField(constraints=[SQL("DEFAULT 0")])
    chain_battle_ranking_gift_set_id = BigIntegerField(index=True)
    created_at = DateTimeField()
    description = CharField()
    gift_description = CharField()
    item_id = BigIntegerField()
    item_type = CharField()
    quantity = IntegerField()
    updated_at = DateTimeField()

    class Meta:
        table_name = 'chain_battle_ranking_gifts'


class Characters(BaseModel):
    created_at = DateTimeField()
    name = CharField()
    race = IntegerField(constraints=[SQL("DEFAULT 0")])
    sex = IntegerField(constraints=[SQL("DEFAULT 0")])
    size = IntegerField(constraints=[SQL("DEFAULT 0")])
    updated_at = DateTimeField()

    class Meta:
        table_name = 'characters'


class ClientSettings(BaseModel):
    created_at = DateTimeField()
    key = CharField(primary_key=True)
    updated_at = DateTimeField()
    value = CharField()

    class Meta:
        table_name = 'client_settings'


class CollectionCards(BaseModel):
    card_id = IntegerField()
    collection_unique_id = IntegerField()
    created_at = DateTimeField()
    event_id = IntegerField(null=True)
    priority = IntegerField(constraints=[SQL("DEFAULT 0")])
    updated_at = DateTimeField()

    class Meta:
        table_name = 'collection_cards'
        indexes = (
            (('collection_unique_id', 'card_id'), True),
        )


class CollectionCategories(BaseModel):
    created_at = DateTimeField()
    name = CharField()
    priority = IntegerField(constraints=[SQL("DEFAULT 0")])
    updated_at = DateTimeField()

    class Meta:
        table_name = 'collection_categories'


class CollectionUniques(BaseModel):
    background_id = IntegerField()
    card_id = IntegerField()
    collection_category_id = IntegerField()
    created_at = DateTimeField()
    name = CharField()
    priority = IntegerField(constraints=[SQL("DEFAULT 0")])
    updated_at = DateTimeField()

    class Meta:
        table_name = 'collection_uniques'
        indexes = (
            (('collection_category_id', 'name'), True),
        )


class DbStories(BaseModel):
    banner_image_path = CharField(null=True)
    created_at = DateTimeField()
    name = CharField()
    priority = IntegerField()
    updated_at = DateTimeField()

    class Meta:
        table_name = 'db_stories'


class DialogBodies(BaseModel):
    created_at = DateTimeField()
    description = TextField(null=True)
    updated_at = DateTimeField()

    class Meta:
        table_name = 'dialog_bodies'


class Dialogs(BaseModel):
    created_at = DateTimeField()
    dialog_body_ids = UnknownField()  # json
    dialog_icon_type = CharField(null=True)
    updated_at = DateTimeField()

    class Meta:
        table_name = 'dialogs'


class DotCharacterGrowths(BaseModel):
    created_at = DateTimeField()
    grow_type = IntegerField()
    image_number = IntegerField()
    label_name = CharField(null=True)
    lv = IntegerField()
    point_total = IntegerField()
    updated_at = DateTimeField()

    class Meta:
        table_name = 'dot_character_growths'
        indexes = (
            (('grow_type', 'lv'), True),
        )


class DotCharacters(BaseModel):
    character_number = IntegerField()
    created_at = DateTimeField()
    end_at = DateTimeField()
    grow_type = IntegerField()
    max_lv = IntegerField()
    name = CharField()
    start_at = DateTimeField()
    updated_at = DateTimeField()

    class Meta:
        table_name = 'dot_characters'


class EffectPacks(BaseModel):
    alpha = IntegerField()
    blue = IntegerField()
    category = IntegerField()
    created_at = DateTimeField()
    green = IntegerField()
    lite_flicker_rate = IntegerField(constraints=[SQL("DEFAULT 0")])
    name = CharField()
    pack_name = CharField()
    red = IntegerField()
    scene_name = CharField()
    updated_at = DateTimeField()

    class Meta:
        table_name = 'effect_packs'


class EnemyAiConditions(BaseModel):
    action_type = IntegerField(constraints=[SQL("DEFAULT 0")])
    ai_param = IntegerField(null=True)
    ai_param2 = IntegerField(null=True)
    ai_type = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    atk_rate_1 = IntegerField(constraints=[SQL("DEFAULT 100")])
    atk_rate_2 = IntegerField(constraints=[SQL("DEFAULT 100")])
    attack_order = IntegerField(constraints=[SQL("DEFAULT -1")])
    created_at = DateTimeField()
    hp_rate_begin = FloatField(constraints=[SQL("DEFAULT 0.0")])
    hp_rate_end = FloatField(constraints=[SQL("DEFAULT 0.0")])
    max_num_per_turn = IntegerField(constraints=[SQL("DEFAULT 1")])
    max_number = IntegerField(constraints=[SQL("DEFAULT 0")])
    min_interval = IntegerField(constraints=[SQL("DEFAULT 0")])
    next_ai_type = IntegerField(null=True)
    recover_hp_rate = IntegerField(constraints=[SQL("DEFAULT 0")])
    updated_at = DateTimeField()
    weight = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'enemy_ai_conditions'


class EnemySkills(BaseModel):
    causality_conditions = TextField(null=True)
    created_at = DateTimeField()
    description = CharField(null=True)
    eff_value1 = IntegerField(null=True)
    eff_value2 = IntegerField(null=True)
    eff_value3 = IntegerField(null=True)
    efficacy_type = IntegerField()
    exec_timing_type = IntegerField(constraints=[SQL("DEFAULT 0")])
    icon_type = IntegerField(constraints=[SQL("DEFAULT 0")])
    name = CharField()
    probability = IntegerField(constraints=[SQL("DEFAULT 0")])
    sub_target_type_set_id = IntegerField(constraints=[SQL("DEFAULT 0")])
    target_type = IntegerField(constraints=[SQL("DEFAULT 0")])
    target_value1 = IntegerField(constraints=[SQL("DEFAULT 0")])
    target_value2 = IntegerField(constraints=[SQL("DEFAULT 0")])
    target_value3 = IntegerField(constraints=[SQL("DEFAULT 0")])
    turn = IntegerField(constraints=[SQL("DEFAULT 0")])
    updated_at = DateTimeField()

    class Meta:
        table_name = 'enemy_skills'


class EquipmentSkillItems(BaseModel):
    attack = IntegerField(constraints=[SQL("DEFAULT 0")])
    created_at = DateTimeField()
    defense = IntegerField(constraints=[SQL("DEFAULT 0")])
    description = TextField()
    equipment_skill_limitation_set_id = BigIntegerField(null=True)
    grade = CharField()
    hp = IntegerField(constraints=[SQL("DEFAULT 0")])
    icon_image_id = IntegerField()
    is_eternal = IntegerField(constraints=[SQL("DEFAULT 0")])
    name = CharField()
    selling_exchange_point = IntegerField(constraints=[SQL("DEFAULT 0")])
    updated_at = DateTimeField()

    class Meta:
        table_name = 'equipment_skill_items'


class EquipmentSkillLimitations(BaseModel):
    conditions = UnknownField()  # json
    created_at = DateTimeField()
    equipment_skill_limitation_set_id = BigIntegerField(index=True)
    type = CharField()
    updated_at = DateTimeField()

    class Meta:
        table_name = 'equipment_skill_limitations'


class EquipmentSkills(BaseModel):
    created_at = DateTimeField()
    equipment_skill_item_id = BigIntegerField()
    level = IntegerField()
    potential_skill_id = BigIntegerField(null=True)
    status_type = CharField(null=True)
    updated_at = DateTimeField()

    class Meta:
        table_name = 'equipment_skills'


class EventkagiItems(BaseModel):
    area_category_ids = UnknownField(null=True)  # json
    created_at = DateTimeField()
    description = CharField()
    name = CharField()
    rarity = IntegerField(constraints=[SQL("DEFAULT 0")])
    selling_exchange_point = IntegerField(constraints=[SQL("DEFAULT 0")])
    updated_at = DateTimeField()

    class Meta:
        table_name = 'eventkagi_items'


class ExchangeableItems(BaseModel):
    created_at = DateTimeField()
    quantity = IntegerField()
    treasure_item_id = BigIntegerField(index=True)
    updated_at = DateTimeField()

    class Meta:
        table_name = 'exchangeable_items'


class ForcedScripts(BaseModel):
    created_at = DateTimeField()
    script_id = IntegerField(constraints=[SQL("DEFAULT 0")], unique=True)
    updated_at = DateTimeField()

    class Meta:
        table_name = 'forced_scripts'


class HelpBodies(BaseModel):
    created_at = DateTimeField()
    description = TextField(null=True)
    help_id = IntegerField(index=True, null=True)
    image_path = CharField(null=True)
    updated_at = DateTimeField()

    class Meta:
        table_name = 'help_bodies'


class HelpCategories(BaseModel):
    created_at = DateTimeField()
    num = IntegerField(null=True)
    title = CharField()
    updated_at = DateTimeField()

    class Meta:
        table_name = 'help_categories'


class Helps(BaseModel):
    created_at = DateTimeField()
    description = TextField(null=True)
    help_category_id = IntegerField(index=True)
    num = IntegerField(null=True)
    title = CharField()
    updated_at = DateTimeField()

    class Meta:
        table_name = 'helps'


class ItemCardProperties(BaseModel):
    card_id = BigIntegerField(index=True)
    created_at = DateTimeField()
    exp = IntegerField()
    updated_at = DateTimeField()

    class Meta:
        table_name = 'item_card_properties'


class LayoutPermissions(BaseModel):
    created_at = DateTimeField()
    parts_name = CharField()
    status = IntegerField(constraints=[SQL("DEFAULT 1")])
    updated_at = DateTimeField()

    class Meta:
        table_name = 'layout_permissions'


class LeaderSkillSets(BaseModel):
    created_at = DateTimeField()
    description = TextField()
    name = CharField()
    updated_at = DateTimeField()

    class Meta:
        table_name = 'leader_skill_sets'


class LeaderSkills(BaseModel):
    calc_option = IntegerField(constraints=[SQL("DEFAULT 0")])
    causality_conditions = TextField(null=True)
    created_at = DateTimeField()
    efficacy_type = IntegerField(constraints=[SQL("DEFAULT 0")])
    efficacy_values = UnknownField(null=True)  # json
    exec_timing_type = IntegerField(constraints=[SQL("DEFAULT 0")])
    leader_skill_set_id = BigIntegerField(index=True)
    sub_target_type_set_id = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    target_type = IntegerField(constraints=[SQL("DEFAULT 0")])
    updated_at = DateTimeField()

    class Meta:
        table_name = 'leader_skills'


class LevelBgs(BaseModel):
    bg1_coef = IntegerField(constraints=[SQL("DEFAULT 0")])
    bg1_enable = IntegerField(constraints=[SQL("DEFAULT 0")])
    bg1_flip_disable = IntegerField(constraints=[SQL("DEFAULT 0")])
    bg2_coef = IntegerField(constraints=[SQL("DEFAULT 0")])
    bg2_enable = IntegerField(constraints=[SQL("DEFAULT 0")])
    bg2_flip_disable = IntegerField(constraints=[SQL("DEFAULT 0")])
    bg3_coef = IntegerField(constraints=[SQL("DEFAULT 0")])
    bg3_enable = IntegerField(constraints=[SQL("DEFAULT 0")])
    bg3_flip_disable = IntegerField(constraints=[SQL("DEFAULT 0")])
    bg4_coef = IntegerField(constraints=[SQL("DEFAULT 0")])
    bg4_enable = IntegerField(constraints=[SQL("DEFAULT 0")])
    bg4_flip_disable = IntegerField(constraints=[SQL("DEFAULT 0")])
    created_at = DateTimeField()
    name = CharField()
    updated_at = DateTimeField()

    class Meta:
        table_name = 'level_bgs'


class LinkSkillEfficacies(BaseModel):
    calc_option = IntegerField(constraints=[SQL("DEFAULT 0")])
    created_at = DateTimeField()
    eff_value1 = FloatField(constraints=[SQL("DEFAULT 0.0")])
    eff_value2 = FloatField(constraints=[SQL("DEFAULT 0.0")])
    eff_value3 = FloatField(constraints=[SQL("DEFAULT 0.0")])
    efficacy_type = IntegerField(constraints=[SQL("DEFAULT 0")])
    link_check_type = IntegerField(constraints=[SQL("DEFAULT 0")])
    link_skill_lv_id = BigIntegerField(index=True)
    lnk_value1 = IntegerField(constraints=[SQL("DEFAULT 0")])
    lnk_value2 = IntegerField(constraints=[SQL("DEFAULT 0")])
    lnk_value3 = IntegerField(constraints=[SQL("DEFAULT 0")])
    sub_target_type_set_id = IntegerField(constraints=[SQL("DEFAULT 0")])
    target_type = IntegerField(constraints=[SQL("DEFAULT 0")])
    turn = IntegerField(constraints=[SQL("DEFAULT 0")])
    updated_at = DateTimeField()

    class Meta:
        table_name = 'link_skill_efficacies'


class LinkSkillLvs(BaseModel):
    created_at = DateTimeField()
    description = CharField(null=True)
    link_skill_id = BigIntegerField(index=True, null=True)
    skill_lv = IntegerField(index=True)
    updated_at = DateTimeField()

    class Meta:
        table_name = 'link_skill_lvs'


class LinkSkills(BaseModel):
    created_at = DateTimeField()
    description = CharField()
    kana = CharField(null=True)
    link_skill_lv_up_prob_set_id = IntegerField()
    name = CharField()
    need_link_num = IntegerField(constraints=[SQL("DEFAULT 0")])
    updated_at = DateTimeField()

    class Meta:
        table_name = 'link_skills'


class Marquees(BaseModel):
    created_at = DateTimeField()
    description = TextField()
    scene_name = CharField(unique=True)
    updated_at = DateTimeField()

    class Meta:
        table_name = 'marquees'


class MissionBoardCampaigns(BaseModel):
    banner_image_path = CharField()
    campaign_complete_mission_id = BigIntegerField()
    complete_image_path = CharField()
    complete_link_to = CharField(null=True)
    complete_message = TextField()
    created_at = DateTimeField()
    end_at = DateTimeField()
    name = CharField()
    start_at = DateTimeField()
    updated_at = DateTimeField()

    class Meta:
        table_name = 'mission_board_campaigns'


class MissionBoards(BaseModel):
    background_image_path = CharField()
    complete_mission_id = BigIntegerField()
    contents_lv = IntegerField(null=True)
    created_at = DateTimeField()
    mission_board_campaign_id = BigIntegerField(index=True)
    mission_category_id = BigIntegerField(index=True)
    number = IntegerField()
    popup_id = BigIntegerField(null=True)
    updated_at = DateTimeField()

    class Meta:
        table_name = 'mission_boards'


class MissionCategories(BaseModel):
    created_at = DateTimeField()
    dragonball_session_id = IntegerField(null=True)
    image_path = CharField(null=True)
    name = CharField()
    priority = IntegerField(constraints=[SQL("DEFAULT 0")])
    type = CharField(null=True)
    updated_at = DateTimeField()

    class Meta:
        table_name = 'mission_categories'


class MissionCategoryRewards(BaseModel):
    created_at = DateTimeField()
    item1_id = BigIntegerField(null=True)
    item1_type = CharField(null=True)
    item2_id = BigIntegerField(null=True)
    item2_type = CharField(null=True)
    item3_id = BigIntegerField(null=True)
    item3_type = CharField(null=True)
    item4_id = BigIntegerField(null=True)
    item4_type = CharField(null=True)
    mission_category_id = BigIntegerField(index=True)
    updated_at = DateTimeField()

    class Meta:
        table_name = 'mission_category_rewards'


class MissionPeriods(BaseModel):
    created_at = DateTimeField()
    dot_character_point = IntegerField(constraints=[SQL("DEFAULT 0")])
    mission_id = IntegerField(unique=True)
    type = CharField(null=True)
    updated_at = DateTimeField()
    wday = IntegerField(null=True)
    wday_hours_to_end = IntegerField(null=True)
    wday_start_at = CharField(null=True)

    class Meta:
        table_name = 'mission_periods'


class MissionRewards(BaseModel):
    announcement_label = CharField(null=True)
    announcement_priority = IntegerField(null=True)
    card_exp_init = IntegerField(constraints=[SQL("DEFAULT 0")])
    created_at = DateTimeField()
    item_id = IntegerField()
    item_type = CharField()
    mission_id = IntegerField(index=True)
    quantity = IntegerField(constraints=[SQL("DEFAULT 0")])
    updated_at = DateTimeField()

    class Meta:
        table_name = 'mission_rewards'


class Missions(BaseModel):
    area_id = IntegerField(index=True, null=True)
    conditions = UnknownField(null=True)  # json
    created_at = DateTimeField()
    description = TextField()
    display_target_value = IntegerField(null=True)
    end_at = DateTimeField()
    end_at_hidden = IntegerField(constraints=[SQL("DEFAULT 0")])
    link_to = CharField(null=True)
    mission_category_id = IntegerField(index=True)
    name = CharField()
    orderer_id = IntegerField(constraints=[SQL("DEFAULT 0")])
    panel_name = CharField(null=True)
    priority = IntegerField(constraints=[SQL("DEFAULT 0")])
    start_at = DateTimeField()
    target_100_value = IntegerField(null=True)
    target_value = IntegerField(constraints=[SQL("DEFAULT 0")])
    type = CharField(null=True)
    updated_at = DateTimeField()
    z_battle_stage_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = 'missions'
        indexes = (
            (('type', 'start_at', 'end_at'), False),
        )


class OptimalAwakeningGrowths(BaseModel):
    leader_skill_set_id = BigIntegerField(index=True, null=True)
    lv_max = IntegerField()
    optimal_awakening_grow_type = IntegerField()
    passive_skill_set_id = IntegerField(null=True)
    skill_lv_max = IntegerField()
    step = IntegerField()

    class Meta:
        table_name = 'optimal_awakening_growths'
        indexes = (
            (('optimal_awakening_grow_type', 'step'), True),
        )


class PassiveSkillEffects(BaseModel):
    bgm_id = IntegerField(null=True)
    created_at = DateTimeField()
    lite_flicker_rate = IntegerField(constraints=[SQL("DEFAULT 0")])
    script_name = CharField()
    updated_at = DateTimeField()

    class Meta:
        table_name = 'passive_skill_effects'


class PassiveSkillSetRelations(BaseModel):
    created_at = DateTimeField()
    passive_skill_id = IntegerField()
    passive_skill_set_id = IntegerField(index=True)
    updated_at = DateTimeField()

    class Meta:
        table_name = 'passive_skill_set_relations'


class PassiveSkillSets(BaseModel):
    created_at = DateTimeField()
    description = TextField(null=True)
    name = CharField(null=True)
    updated_at = DateTimeField()

    class Meta:
        table_name = 'passive_skill_sets'


class PassiveSkills(BaseModel):
    calc_option = IntegerField(constraints=[SQL("DEFAULT 0")])
    causality_conditions = TextField(null=True)
    created_at = DateTimeField()
    description = TextField()
    eff_value1 = IntegerField(constraints=[SQL("DEFAULT 0")])
    eff_value2 = IntegerField(constraints=[SQL("DEFAULT 0")])
    eff_value3 = IntegerField(constraints=[SQL("DEFAULT 0")])
    efficacy_type = IntegerField(constraints=[SQL("DEFAULT 0")])
    exec_timing_type = IntegerField(constraints=[SQL("DEFAULT 0")])
    is_once = IntegerField(constraints=[SQL("DEFAULT 0")])
    name = CharField()
    passive_skill_effect_id = BigIntegerField(index=True, null=True)
    probability = IntegerField(constraints=[SQL("DEFAULT 0")])
    sub_target_type_set_id = IntegerField(constraints=[SQL("DEFAULT 0")])
    target_type = IntegerField(constraints=[SQL("DEFAULT 0")])
    turn = IntegerField(constraints=[SQL("DEFAULT 0")])
    updated_at = DateTimeField()

    class Meta:
        table_name = 'passive_skills'


class Points(BaseModel):
    amount = IntegerField(constraints=[SQL("DEFAULT 0")])
    created_at = DateTimeField()
    type = CharField(null=True)
    updated_at = DateTimeField()

    class Meta:
        table_name = 'points'


class PotentialBoards(BaseModel):
    comment = CharField(null=True)
    created_at = DateTimeField()
    updated_at = DateTimeField()

    class Meta:
        table_name = 'potential_boards'


class PotentialEventSelectionTables(BaseModel):
    comment = CharField(null=True)
    created_at = DateTimeField()
    required_stone_for_unrelease = IntegerField()
    updated_at = DateTimeField()

    class Meta:
        table_name = 'potential_event_selection_tables'


class PotentialEventSelections(BaseModel):
    created_at = DateTimeField()
    event_id = IntegerField()
    selection_table_id = IntegerField()
    updated_at = DateTimeField()

    class Meta:
        table_name = 'potential_event_selections'


class PotentialEvents(BaseModel):
    additional_value = IntegerField(constraints=[SQL("DEFAULT 0")])
    created_at = DateTimeField()
    currency_id = IntegerField(null=True)
    type = CharField()
    updated_at = DateTimeField()

    class Meta:
        table_name = 'potential_events'


class PotentialItems(BaseModel):
    created_at = DateTimeField()
    description = CharField()
    is_exclusive = IntegerField(constraints=[SQL("DEFAULT 0")])
    name = CharField()
    rarity = IntegerField(constraints=[SQL("DEFAULT 0")])
    selling_exchange_point = IntegerField(constraints=[SQL("DEFAULT 0")])
    updated_at = DateTimeField()

    class Meta:
        table_name = 'potential_items'


class PotentialSkillLvValues(BaseModel):
    created_at = DateTimeField()
    lv = IntegerField()
    potential_skill_id = IntegerField()
    updated_at = DateTimeField()
    value = IntegerField()

    class Meta:
        table_name = 'potential_skill_lv_values'
        indexes = (
            (('potential_skill_id', 'lv'), True),
        )


class PotentialSkills(BaseModel):
    calc_option = IntegerField(constraints=[SQL("DEFAULT 0")])
    causality_conditions = TextField(null=True)
    created_at = DateTimeField()
    description = TextField()
    eff_value1 = IntegerField(constraints=[SQL("DEFAULT 0")])
    eff_value2 = IntegerField(constraints=[SQL("DEFAULT 0")])
    eff_value3 = IntegerField(constraints=[SQL("DEFAULT 0")])
    efficacy_type = IntegerField(constraints=[SQL("DEFAULT 0")])
    exec_timing_type = IntegerField(constraints=[SQL("DEFAULT 0")])
    is_once = IntegerField(constraints=[SQL("DEFAULT 0")])
    name = CharField()
    probability = IntegerField(constraints=[SQL("DEFAULT 0")])
    target_type = IntegerField(constraints=[SQL("DEFAULT 0")])
    turn = IntegerField(constraints=[SQL("DEFAULT 0")])
    updated_at = DateTimeField()
    variable_column = CharField(constraints=[SQL("DEFAULT 'eff_value1'")])

    class Meta:
        table_name = 'potential_skills'


class PotentialSquareConditionSetRelations(BaseModel):
    condition_id = IntegerField()
    condition_set_id = IntegerField()
    created_at = DateTimeField()
    updated_at = DateTimeField()

    class Meta:
        table_name = 'potential_square_condition_set_relations'


class PotentialSquareConditionSets(BaseModel):
    comment = CharField(null=True)
    created_at = DateTimeField()
    updated_at = DateTimeField()

    class Meta:
        table_name = 'potential_square_condition_sets'


class PotentialSquareConditions(BaseModel):
    comment = CharField(null=True)
    conditions = UnknownField(null=True)  # json
    created_at = DateTimeField()
    type = CharField()
    updated_at = DateTimeField()

    class Meta:
        table_name = 'potential_square_conditions'


class PotentialSquareRelations(BaseModel):
    created_at = DateTimeField()
    potential_square_id = IntegerField(index=True)
    prev_potential_square_id = IntegerField(null=True)
    updated_at = DateTimeField()

    class Meta:
        table_name = 'potential_square_relations'


class PotentialSquares(BaseModel):
    condition_set_id = IntegerField()
    created_at = DateTimeField()
    event_id = IntegerField()
    is_locked = IntegerField(constraints=[SQL("DEFAULT 0")])
    potential_board_id = IntegerField()
    route = IntegerField(null=True)
    updated_at = DateTimeField()

    class Meta:
        table_name = 'potential_squares'


class QuestCategoryBonusGroups(BaseModel):
    created_at = DateTimeField()
    description = TextField(null=True)
    name = CharField()
    quest_category_bonus_type = CharField(unique=True)
    updated_at = DateTimeField()

    class Meta:
        table_name = 'quest_category_bonus_groups'


class QuestCategoryBonusRarityTables(BaseModel):
    created_at = DateTimeField()
    description = CharField()
    rarity_lr = IntegerField()
    rarity_n = IntegerField()
    rarity_r = IntegerField()
    rarity_sr = IntegerField()
    rarity_ssr = IntegerField()
    rarity_ur = IntegerField()
    updated_at = DateTimeField()

    class Meta:
        table_name = 'quest_category_bonus_rarity_tables'


class QuestCategoryBonuses(BaseModel):
    card_category_id = IntegerField()
    created_at = DateTimeField()
    quest_category_bonus_rarity_table_id = IntegerField(null=True)
    quest_id = IntegerField(index=True)
    type = CharField()
    updated_at = DateTimeField()

    class Meta:
        table_name = 'quest_category_bonuses'


class Quests(BaseModel):
    all_clear_bonus_stones = IntegerField(null=True)
    any_clear_bonus_stones = IntegerField(null=True)
    area_id = IntegerField(index=True)
    boostable = IntegerField(constraints=[SQL("DEFAULT 0")])
    can_ignore_difficulty_order = IntegerField(constraints=[SQL("DEFAULT 0")])
    created_at = DateTimeField()
    enable_battle_auto = IntegerField(constraints=[SQL("DEFAULT 1")])
    enable_sugoroku_auto = IntegerField(constraints=[SQL("DEFAULT 1")])
    icon_x = IntegerField(null=True)
    icon_y = IntegerField(null=True)
    interval_reset_visited_days = IntegerField(null=True)
    limitation_announcement_master_id = IntegerField(null=True)
    name = CharField()
    prev_quest_id = IntegerField(index=True, null=True)
    start_at = DateTimeField()
    updated_at = DateTimeField()
    visit_count_max = IntegerField(null=True)

    class Meta:
        table_name = 'quests'
        indexes = (
            (('area_id', 'prev_quest_id'), True),
        )


class RankRanges(BaseModel):
    created_at = DateTimeField()
    max = IntegerField()
    min = IntegerField()
    type = CharField(null=True)
    updated_at = DateTimeField()

    class Meta:
        table_name = 'rank_ranges'


class RankStatuses(BaseModel):
    act_max = IntegerField()
    created_at = DateTimeField()
    exp_total = IntegerField(unique=True)
    friends_capacity = IntegerField()
    rank = IntegerField(unique=True)
    updated_at = DateTimeField()

    class Meta:
        table_name = 'rank_statuses'


class RelatedCardCategories(BaseModel):
    card_category_id = IntegerField()
    created_at = DateTimeField()
    enemy_skill_id = IntegerField()
    updated_at = DateTimeField()

    class Meta:
        table_name = 'related_card_categories'


class RelatedLinkSkills(BaseModel):
    created_at = DateTimeField()
    enemy_skill_id = IntegerField()
    link_skill_id = IntegerField()
    updated_at = DateTimeField()

    class Meta:
        table_name = 'related_link_skills'
        indexes = (
            (('enemy_skill_id', 'link_skill_id'), True),
        )


class RelatedPassiveSkillSets(BaseModel):
    created_at = DateTimeField()
    enemy_skill_id = IntegerField()
    passive_skill_set_id = IntegerField()
    updated_at = DateTimeField()

    class Meta:
        table_name = 'related_passive_skill_sets'
        indexes = (
            (('enemy_skill_id', 'passive_skill_set_id'), True),
        )


class RmbattleBgmPatterns(BaseModel):
    boss_bgm_id = IntegerField()
    created_at = DateTimeField()
    last_boss_bgm_id = IntegerField()
    normal_bgm_id = IntegerField()
    updated_at = DateTimeField()

    class Meta:
        table_name = 'rmbattle_bgm_patterns'


class RmbattleHelpBodies(BaseModel):
    created_at = DateTimeField()
    description = TextField(null=True)
    image_path = CharField(null=True)
    rmbattle_help_id = IntegerField(index=True)
    updated_at = DateTimeField()

    class Meta:
        table_name = 'rmbattle_help_bodies'


class RmbattleHelpCategories(BaseModel):
    created_at = DateTimeField()
    num = IntegerField(null=True)
    title = CharField()
    updated_at = DateTimeField()

    class Meta:
        table_name = 'rmbattle_help_categories'


class RmbattleHelps(BaseModel):
    created_at = DateTimeField()
    description = TextField(null=True)
    num = IntegerField(null=True)
    rmbattle_help_category_id = IntegerField(index=True)
    title = CharField()
    updated_at = DateTimeField()

    class Meta:
        table_name = 'rmbattle_helps'


class RmbattleMissionRewards(BaseModel):
    card_exp_init = IntegerField()
    created_at = DateTimeField()
    description = CharField()
    gift_description = CharField()
    item_id = IntegerField()
    item_type = CharField()
    quantity = IntegerField()
    rmbattle_mission_id = IntegerField(index=True)
    updated_at = DateTimeField()

    class Meta:
        table_name = 'rmbattle_mission_rewards'


class RmbattleMissions(BaseModel):
    conditions = UnknownField()  # json
    created_at = DateTimeField()
    is_attention = IntegerField(constraints=[SQL("DEFAULT 0")])
    name = CharField()
    priority = IntegerField()
    rmbattle_id = IntegerField()
    target_value = IntegerField(null=True)
    type = CharField()
    updated_at = DateTimeField()

    class Meta:
        table_name = 'rmbattle_missions'
        indexes = (
            (('rmbattle_id', 'type'), False),
        )


class SdArenas(BaseModel):
    background_image_id = IntegerField()
    created_at = DateTimeField()
    position_x = IntegerField()
    position_y = IntegerField()
    sd_map_id = BigIntegerField(index=True)
    symbol_item_id = IntegerField()
    symbol_item_type = CharField()
    updated_at = DateTimeField()

    class Meta:
        table_name = 'sd_arenas'


class SdCharacters(BaseModel):
    attack = IntegerField()
    card_id = BigIntegerField(unique=True)
    created_at = DateTimeField()
    description = TextField(null=True)
    element = IntegerField()
    hp = IntegerField()
    number = IntegerField()
    open_at = DateTimeField()
    rarity = IntegerField()
    series = IntegerField()
    updated_at = DateTimeField()

    class Meta:
        table_name = 'sd_characters'
        indexes = (
            (('series', 'number'), True),
        )


class SdHelpBodies(BaseModel):
    created_at = DateTimeField()
    description = TextField(null=True)
    image_path = CharField(null=True)
    sd_help_id = BigIntegerField(index=True)
    updated_at = DateTimeField()

    class Meta:
        table_name = 'sd_help_bodies'


class SdHelpCategories(BaseModel):
    created_at = DateTimeField()
    num = IntegerField(null=True)
    title = CharField()
    updated_at = DateTimeField()

    class Meta:
        table_name = 'sd_help_categories'


class SdHelps(BaseModel):
    created_at = DateTimeField()
    description = TextField(null=True)
    num = IntegerField(null=True)
    sd_help_category_id = BigIntegerField(index=True)
    title = CharField()
    updated_at = DateTimeField()

    class Meta:
        table_name = 'sd_helps'


class SdMaps(BaseModel):
    background_image_id = IntegerField()
    created_at = DateTimeField()
    updated_at = DateTimeField()

    class Meta:
        table_name = 'sd_maps'


class SdPacks(BaseModel):
    created_at = DateTimeField()
    description = CharField()
    name = CharField()
    updated_at = DateTimeField()

    class Meta:
        table_name = 'sd_packs'


class SdStages(BaseModel):
    created_at = DateTimeField()
    position_x = IntegerField()
    position_y = IntegerField()
    respawn_minutes = IntegerField()
    sd_arena_id = BigIntegerField(index=True)
    sd_enemy_table_id = BigIntegerField()
    updated_at = DateTimeField()

    class Meta:
        table_name = 'sd_stages'


class Shops(BaseModel):
    close_at = DateTimeField()
    created_at = DateTimeField()
    end_at = DateTimeField()
    item_change_interval_sec = IntegerField(null=True)
    open_at = DateTimeField()
    required_stone_to_change_item = IntegerField(null=True)
    start_at = DateTimeField()
    type = CharField(null=True)
    updated_at = DateTimeField()

    class Meta:
        table_name = 'shops'


class SkillCausalities(BaseModel):
    cau_val1 = IntegerField(constraints=[SQL("DEFAULT 0")])
    cau_val2 = IntegerField(constraints=[SQL("DEFAULT 0")])
    cau_val3 = IntegerField(constraints=[SQL("DEFAULT 0")])
    causality_type = IntegerField(constraints=[SQL("DEFAULT 0")])
    created_at = DateTimeField()
    updated_at = DateTimeField()

    class Meta:
        table_name = 'skill_causalities'


class SkillGroupRelations(BaseModel):
    created_at = DateTimeField()
    skill_group_id = BigIntegerField()
    target_id = BigIntegerField()
    target_type = CharField()
    updated_at = DateTimeField()

    class Meta:
        table_name = 'skill_group_relations'
        indexes = (
            (('target_type', 'target_id', 'skill_group_id'), True),
        )
        primary_key = False


class SkillGroups(BaseModel):
    created_at = DateTimeField()
    name = CharField()
    priority = IntegerField()
    updated_at = DateTimeField()

    class Meta:
        table_name = 'skill_groups'


class SkillLabels(BaseModel):
    created_at = DateTimeField()
    efficacy_type = IntegerField(constraints=[SQL("DEFAULT 0")])
    is_display = IntegerField(constraints=[SQL("DEFAULT 0")])
    updated_at = DateTimeField()

    class Meta:
        table_name = 'skill_labels'


class SoundEffectOffsets(BaseModel):
    created_at = DateTimeField()
    sound_effect_id = IntegerField()
    sound_effect_set_id = IntegerField(index=True)
    start_offset_millisecond = IntegerField()
    updated_at = DateTimeField()

    class Meta:
        table_name = 'sound_effect_offsets'


class SpecialBonuses(BaseModel):
    calc_option = IntegerField(null=True)
    causality_conditions = TextField(null=True)
    created_at = DateTimeField()
    description = CharField(null=True)
    eff_value1 = IntegerField(null=True)
    eff_value2 = IntegerField(null=True)
    eff_value3 = IntegerField(null=True)
    efficacy_type = IntegerField(null=True)
    name = CharField(null=True)
    probability = IntegerField(null=True)
    target_type = IntegerField(null=True)
    turn = IntegerField(null=True)
    updated_at = DateTimeField()

    class Meta:
        table_name = 'special_bonuses'


class SpecialCategories(BaseModel):
    created_at = DateTimeField()
    display_order = IntegerField(constraints=[SQL("DEFAULT 0")])
    name = CharField(constraints=[SQL("DEFAULT ''")])
    raw_attribute = IntegerField(constraints=[SQL("DEFAULT 0")], unique=True)
    updated_at = DateTimeField()

    class Meta:
        table_name = 'special_categories'


class SpecialItems(BaseModel):
    created_at = DateTimeField()
    description = TextField(null=True)
    name = CharField(null=True)
    rarity = IntegerField(constraints=[SQL("DEFAULT 0")])
    selling_exchange_point = IntegerField(constraints=[SQL("DEFAULT 0")])
    updated_at = DateTimeField()

    class Meta:
        table_name = 'special_items'


class SpecialSets(BaseModel):
    aim_target = IntegerField(constraints=[SQL("DEFAULT 0")])
    causality_description = TextField(null=True)
    created_at = DateTimeField()
    description = CharField()
    increase_rate = IntegerField(constraints=[SQL("DEFAULT 0")])
    lv_bonus = IntegerField(constraints=[SQL("DEFAULT 0")])
    name = CharField()
    updated_at = DateTimeField()

    class Meta:
        table_name = 'special_sets'


class SpecialViews(BaseModel):
    created_at = DateTimeField()
    cut_in_card_id = IntegerField(constraints=[SQL("DEFAULT 0")])
    energy_color = IntegerField(null=True)
    lite_flicker_rate = IntegerField(constraints=[SQL("DEFAULT 0")])
    script_name = CharField()
    special_category_id = IntegerField(index=True, null=True)
    special_motion = IntegerField(constraints=[SQL("DEFAULT 0")])
    special_name_no = IntegerField(constraints=[SQL("DEFAULT 0")])
    updated_at = DateTimeField()

    class Meta:
        table_name = 'special_views'


class Specials(BaseModel):
    calc_option = IntegerField(constraints=[SQL("DEFAULT 0")])
    causality_conditions = TextField(null=True)
    created_at = DateTimeField()
    eff_value1 = IntegerField(constraints=[SQL("DEFAULT 0")])
    eff_value2 = IntegerField(constraints=[SQL("DEFAULT 0")])
    eff_value3 = IntegerField(constraints=[SQL("DEFAULT 0")])
    efficacy_type = IntegerField(constraints=[SQL("DEFAULT 0")])
    prob = IntegerField(constraints=[SQL("DEFAULT 0")])
    special_set_id = IntegerField()
    target_type = IntegerField(constraints=[SQL("DEFAULT 0")])
    turn = IntegerField(constraints=[SQL("DEFAULT 0")])
    type = CharField()
    updated_at = DateTimeField()

    class Meta:
        table_name = 'specials'
        indexes = (
            (('special_set_id', 'type'), False),
        )


class SqliteSequence(BaseModel):
    name = BareField(null=True)
    seq = BareField(null=True)

    class Meta:
        table_name = 'sqlite_sequence'
        primary_key = False


class StatusExtensions(BaseModel):
    amount = IntegerField(constraints=[SQL("DEFAULT 0")])
    created_at = DateTimeField()
    type = CharField(null=True)
    updated_at = DateTimeField()

    class Meta:
        table_name = 'status_extensions'


class SubTargetTypeSets(BaseModel):
    created_at = DateTimeField()
    updated_at = DateTimeField()

    class Meta:
        table_name = 'sub_target_type_sets'


class SubTargetTypes(BaseModel):
    created_at = DateTimeField()
    sub_target_type_set_id = IntegerField(index=True)
    target_value = IntegerField(constraints=[SQL("DEFAULT 0")])
    target_value_type = IntegerField(constraints=[SQL("DEFAULT 0")])
    updated_at = DateTimeField()

    class Meta:
        table_name = 'sub_target_types'


class SugorokuMapPuzzleColors(BaseModel):
    created_at = DateTimeField()
    updated_at = DateTimeField()
    weight_blue = IntegerField(constraints=[SQL("DEFAULT 0")])
    weight_green = IntegerField(constraints=[SQL("DEFAULT 0")])
    weight_purple = IntegerField(constraints=[SQL("DEFAULT 0")])
    weight_rainbow = IntegerField(constraints=[SQL("DEFAULT 0")])
    weight_red = IntegerField(constraints=[SQL("DEFAULT 0")])
    weight_yellow = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'sugoroku_map_puzzle_colors'


class SugorokuMaps(BaseModel):
    act = IntegerField(constraints=[SQL("DEFAULT 0")])
    battle_background_id = IntegerField(constraints=[SQL("DEFAULT 0")])
    battle_bgm_id = IntegerField(constraints=[SQL("DEFAULT 0")])
    boss_bgm_id = IntegerField(constraints=[SQL("DEFAULT 0")])
    created_at = DateTimeField()
    danger_line_hp = IntegerField(constraints=[SQL("DEFAULT 0")])
    dice_id = IntegerField(null=True)
    difficulty = IntegerField(constraints=[SQL("DEFAULT 0")])
    eventkagi_num = IntegerField(constraints=[SQL("DEFAULT 0")])
    finish_script_id = IntegerField(constraints=[SQL("DEFAULT 0")])
    first_focus_step = IntegerField(null=True)
    is_cpu_only = IntegerField(constraints=[SQL("DEFAULT 0")])
    link_skill_lv_up_prob_rate = FloatField(null=True)
    quest_id = IntegerField(null=True)
    start_script_id = IntegerField(constraints=[SQL("DEFAULT 0")])
    sugoroku_bgm_id = IntegerField(constraints=[SQL("DEFAULT 0")])
    sugoroku_map_puzzle_color_id = IntegerField(constraints=[SQL("DEFAULT 0")])
    sugoroku_map_reward_group_id = BigIntegerField(null=True)
    updated_at = DateTimeField()
    user_exp = IntegerField(constraints=[SQL("DEFAULT 0")])
    zeni = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'sugoroku_maps'
        indexes = (
            (('quest_id', 'difficulty'), True),
        )


class SupportFilms(BaseModel):
    created_at = DateTimeField()
    description = TextField()
    name = CharField()
    updated_at = DateTimeField()

    class Meta:
        table_name = 'support_films'


class SupportItems(BaseModel):
    calc_option = IntegerField(constraints=[SQL("DEFAULT 0")])
    created_at = DateTimeField()
    description = CharField()
    eff1_value1 = IntegerField(constraints=[SQL("DEFAULT 0")])
    eff1_value2 = IntegerField(constraints=[SQL("DEFAULT 0")])
    eff1_value3 = IntegerField(constraints=[SQL("DEFAULT 0")])
    eff2_value1 = IntegerField(constraints=[SQL("DEFAULT 0")])
    eff2_value2 = IntegerField(constraints=[SQL("DEFAULT 0")])
    eff2_value3 = IntegerField(constraints=[SQL("DEFAULT 0")])
    efficacy_type1 = IntegerField(constraints=[SQL("DEFAULT 0")])
    efficacy_type2 = IntegerField(constraints=[SQL("DEFAULT 0")])
    ingame_type = IntegerField(constraints=[SQL("DEFAULT 0")])
    max_per_quest = IntegerField(null=True)
    max_per_quest_extended = IntegerField(null=True)
    name = CharField(null=True)
    rarity = IntegerField(constraints=[SQL("DEFAULT 0")])
    selling_exchange_point = IntegerField(constraints=[SQL("DEFAULT 0")])
    target_type = IntegerField(constraints=[SQL("DEFAULT 0")])
    turn = IntegerField(constraints=[SQL("DEFAULT 0")])
    updated_at = DateTimeField()

    class Meta:
        table_name = 'support_items'


class SupportMemories(BaseModel):
    cost = IntegerField()
    created_at = DateTimeField()
    description = TextField()
    lite_flicker_rate = IntegerField(constraints=[SQL("DEFAULT 0")])
    max_exec_count = IntegerField()
    name = CharField()
    priority = IntegerField(constraints=[SQL("DEFAULT 0")])
    script_name = CharField()
    support_film_id = BigIntegerField()
    unlock_quantity = IntegerField()
    updated_at = DateTimeField()

    class Meta:
        table_name = 'support_memories'


class SupportMemorySkills(BaseModel):
    calc_option = IntegerField(constraints=[SQL("DEFAULT 0")])
    causality_conditions = TextField(null=True)
    created_at = DateTimeField()
    description = TextField(null=True)
    efficacy_type = IntegerField(constraints=[SQL("DEFAULT 0")])
    efficacy_values = UnknownField()  # json
    exec_timing_type = IntegerField(constraints=[SQL("DEFAULT 1")])
    name = CharField(null=True)
    probability = IntegerField(constraints=[SQL("DEFAULT 100")])
    sub_target_type_set_id = BigIntegerField()
    support_memory_id = BigIntegerField(index=True)
    target_type = IntegerField(constraints=[SQL("DEFAULT 0")])
    target_type_values = UnknownField(null=True)  # json
    turn = IntegerField(constraints=[SQL("DEFAULT 0")])
    updated_at = DateTimeField()

    class Meta:
        table_name = 'support_memory_skills'


class Tips(BaseModel):
    created_at = DateTimeField()
    description = TextField()
    end_at = DateTimeField(constraints=[SQL("DEFAULT '2030-01-01 00:00:00'")])
    image_name = CharField(null=True)
    start_at = DateTimeField(constraints=[SQL("DEFAULT '2000-01-01 00:00:00'")])
    title = CharField()
    updated_at = DateTimeField()
    weight = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'tips'


class TitleScreens(BaseModel):
    bg_anime = CharField(null=True)
    bgm_id = IntegerField(null=True)
    chara_anime = CharField(null=True)
    created_at = DateTimeField()
    end_at = DateTimeField()
    start_at = DateTimeField()
    updated_at = DateTimeField()

    class Meta:
        table_name = 'title_screens'


class TrainingFields(BaseModel):
    addend = IntegerField(null=True)
    card_training_field_exp_up_prob_id = IntegerField(null=True)
    created_at = DateTimeField()
    description = CharField()
    elements = IntegerField(constraints=[SQL("DEFAULT 0")])
    exp = IntegerField(constraints=[SQL("DEFAULT 0")])
    level_bg_id = IntegerField()
    multiplier = FloatField(null=True)
    name = CharField()
    rarity = IntegerField(constraints=[SQL("DEFAULT 0")])
    selling_exchange_point = IntegerField(constraints=[SQL("DEFAULT 0")])
    updated_at = DateTimeField()
    zeni = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'training_fields'


class TrainingItems(BaseModel):
    created_at = DateTimeField()
    description = CharField()
    element = IntegerField(constraints=[SQL("DEFAULT 0")])
    exp = IntegerField(constraints=[SQL("DEFAULT 0")])
    name = CharField()
    rarity = IntegerField(constraints=[SQL("DEFAULT 0")])
    selling_exchange_point = IntegerField(constraints=[SQL("DEFAULT 0")])
    updated_at = DateTimeField()
    zeni_to_use = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'training_items'


class TransformationDescriptions(BaseModel):
    created_at = DateTimeField()
    description = TextField()
    skill_id = IntegerField()
    skill_type = CharField(constraints=[SQL("DEFAULT ''")])
    updated_at = DateTimeField()

    class Meta:
        table_name = 'transformation_descriptions'
        indexes = (
            (('skill_type', 'skill_id'), True),
        )


class TreasureItems(BaseModel):
    created_at = DateTimeField()
    description = CharField()
    image_suffix_number = IntegerField()
    name = CharField()
    rarity = IntegerField(constraints=[SQL("DEFAULT 0")])
    selling_exchange_point = IntegerField(constraints=[SQL("DEFAULT 0")])
    updated_at = DateTimeField()
    will_expire = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'treasure_items'


class TutorialPhases(BaseModel):
    created_at = DateTimeField()
    number = IntegerField()
    parameters = UnknownField(null=True)  # json
    tutorial_scene_url = CharField()
    updated_at = DateTimeField()

    class Meta:
        table_name = 'tutorial_phases'


class TutorialProcesses(BaseModel):
    created_at = DateTimeField()
    number = IntegerField()
    parameters = UnknownField(null=True)  # json
    process_type = CharField()
    step_id = BigIntegerField(index=True)
    updated_at = DateTimeField()

    class Meta:
        table_name = 'tutorial_processes'


class TutorialSteps(BaseModel):
    created_at = DateTimeField()
    is_resume_point = IntegerField(null=True)
    number = IntegerField()
    phase_id = BigIntegerField(index=True)
    updated_at = DateTimeField()

    class Meta:
        table_name = 'tutorial_steps'


class UltimateSpecials(BaseModel):
    aim_target = IntegerField(constraints=[SQL("DEFAULT 0")])
    created_at = DateTimeField()
    description = CharField()
    increase_rate = IntegerField()
    name = CharField()
    updated_at = DateTimeField()

    class Meta:
        table_name = 'ultimate_specials'


class WallpaperItems(BaseModel):
    created_at = DateTimeField()
    description = CharField(null=True)
    name = CharField(null=True)
    updated_at = DateTimeField()

    class Meta:
        table_name = 'wallpaper_items'


class Worlds(BaseModel):
    bgm_id = IntegerField(null=True)
    created_at = DateTimeField()
    height = IntegerField(null=True)
    layer0 = CharField(null=True)
    layer1 = CharField(null=True)
    layer2 = CharField(null=True)
    layer3 = CharField(null=True)
    name = CharField()
    prev_world_id = IntegerField(null=True)
    split = IntegerField(null=True)
    updated_at = DateTimeField()
    width = IntegerField(null=True)

    class Meta:
        table_name = 'worlds'


class ZBattleCheckPoints(BaseModel):
    act = IntegerField()
    created_at = DateTimeField()
    eventkagi_num = IntegerField(constraints=[SQL("DEFAULT 0")])
    level = IntegerField()
    main_reward_id = IntegerField(null=True)
    updated_at = DateTimeField()
    z_battle_normal_reward_table_group_id = IntegerField()
    z_battle_stage_id = IntegerField(index=True)

    class Meta:
        table_name = 'z_battle_check_points'
        indexes = (
            (('z_battle_stage_id', 'level'), True),
        )


class ZBattleEnemies(BaseModel):
    attack_escalation_type = IntegerField(constraints=[SQL("DEFAULT 0")])
    base_attack = IntegerField(constraints=[SQL("DEFAULT 0")])
    base_defence = IntegerField(constraints=[SQL("DEFAULT 0")])
    base_hp = IntegerField(constraints=[SQL("DEFAULT 0")])
    card_escalation_type = IntegerField(constraints=[SQL("DEFAULT 0")])
    created_at = DateTimeField()
    defence_escalation_type = IntegerField(constraints=[SQL("DEFAULT 0")])
    end_level = IntegerField(null=True)
    hp_escalation_type = IntegerField(constraints=[SQL("DEFAULT 0")])
    ordinal_num = IntegerField(constraints=[SQL("DEFAULT 0")])
    performance_escalation_type = IntegerField(constraints=[SQL("DEFAULT 0")])
    skill_escalation_type = IntegerField(constraints=[SQL("DEFAULT 0")])
    special_attack_escalation_type = IntegerField(constraints=[SQL("DEFAULT 0")])
    start_level = IntegerField(constraints=[SQL("DEFAULT 1")])
    updated_at = DateTimeField()
    z_battle_stage_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = 'z_battle_enemies'


class ZBattleEnemyCardEscalations(BaseModel):
    card_id = IntegerField(constraints=[SQL("DEFAULT 0")])
    created_at = DateTimeField()
    escalation_type = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    level = IntegerField(constraints=[SQL("DEFAULT 0")])
    updated_at = DateTimeField()

    class Meta:
        table_name = 'z_battle_enemy_card_escalations'


class ZBattleEnemySkillEscalations(BaseModel):
    created_at = DateTimeField()
    enemy_skill_id = IntegerField(null=True)
    escalation_type = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    level = IntegerField(constraints=[SQL("DEFAULT 0")])
    updated_at = DateTimeField()

    class Meta:
        table_name = 'z_battle_enemy_skill_escalations'


class ZBattleEnemyStatusEscalations(BaseModel):
    created_at = DateTimeField()
    escalation_type = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    escalation_value = IntegerField(constraints=[SQL("DEFAULT 0")])
    level = IntegerField(constraints=[SQL("DEFAULT 0")])
    updated_at = DateTimeField()

    class Meta:
        table_name = 'z_battle_enemy_status_escalations'


class ZBattleFirstRewardLevelRanges(BaseModel):
    created_at = DateTimeField()
    level = IntegerField()
    main_reward_id = IntegerField(null=True)
    updated_at = DateTimeField()
    z_battle_first_reward_set_id = IntegerField()
    z_battle_stage_id = IntegerField()

    class Meta:
        table_name = 'z_battle_first_reward_level_ranges'
        indexes = (
            (('z_battle_stage_id', 'level'), True),
        )


class ZBattleFirstRewards(BaseModel):
    card_exp_init = IntegerField(constraints=[SQL("DEFAULT 0")])
    created_at = DateTimeField()
    item_id = IntegerField()
    item_type = CharField()
    quantity = IntegerField(constraints=[SQL("DEFAULT 0")])
    updated_at = DateTimeField()
    z_battle_first_reward_set_id = IntegerField(index=True)

    class Meta:
        table_name = 'z_battle_first_rewards'


class ZBattleNormalRewardTables(BaseModel):
    created_at = DateTimeField()
    updated_at = DateTimeField()
    z_battle_normal_reward_table_group_id = IntegerField(index=True)

    class Meta:
        table_name = 'z_battle_normal_reward_tables'


class ZBattleNormalRewards(BaseModel):
    card_exp_init = IntegerField(constraints=[SQL("DEFAULT 0")])
    created_at = DateTimeField()
    item_id = IntegerField()
    item_type = CharField()
    quantity = IntegerField(constraints=[SQL("DEFAULT 0")])
    updated_at = DateTimeField()
    z_battle_normal_reward_table_id = IntegerField(index=True)

    class Meta:
        table_name = 'z_battle_normal_rewards'


class ZBattlePowerupThresholds(BaseModel):
    atk = IntegerField(null=True)
    created_at = DateTimeField()
    def_ = IntegerField(column_name='def', null=True)
    hp = IntegerField(null=True)
    special_atk = IntegerField(null=True)
    updated_at = DateTimeField()
    z_battle_stage_id = IntegerField(index=True)

    class Meta:
        table_name = 'z_battle_powerup_thresholds'


class ZBattlePowerupViews(BaseModel):
    created_at = DateTimeField()
    enemy_skill_efficacy_type = IntegerField(index=True)
    texture_name = CharField()
    updated_at = DateTimeField()

    class Meta:
        table_name = 'z_battle_powerup_views'


class ZBattleStageLevelupViews(BaseModel):
    created_at = DateTimeField()
    scene_name = CharField()
    stage_level = IntegerField(index=True)
    updated_at = DateTimeField()

    class Meta:
        table_name = 'z_battle_stage_levelup_views'


class ZBattleStageViews(BaseModel):
    created_at = DateTimeField()
    enemy_name = CharField()
    enemy_nickname = CharField()
    enemy_resource_id = IntegerField()
    params = CharField()
    updated_at = DateTimeField()
    z_battle_stage_id = IntegerField(index=True)

    class Meta:
        table_name = 'z_battle_stage_views'


class ZBattleStages(BaseModel):
    announcement_id = IntegerField(null=True)
    banner_image_path = CharField(null=True)
    danger_line_hp = IntegerField(constraints=[SQL("DEFAULT 0")])
    enable_battle_auto = IntegerField(constraints=[SQL("DEFAULT 1")])
    end_at = DateTimeField()
    eventkagi_end_at = DateTimeField(null=True)
    eventkagi_start_at = DateTimeField(null=True)
    listbutton_image_path = CharField(null=True)
    priority = IntegerField(constraints=[SQL("DEFAULT 0")])
    start_at = DateTimeField()
    z_battle_stage_effect_escalation_type = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'z_battle_stages'
        indexes = (
            (('eventkagi_start_at', 'eventkagi_end_at'), False),
        )
