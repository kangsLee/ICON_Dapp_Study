from iconservice import *

TAG = 'PickDol'

class PickDol(IconScoreBase):
    # _FAN_DICT = '_FAN_DICT'
    _FAN_TOTAL_VOTE_DICT = 'FAN_TOTAL_VOTE_DICT'
    _FAN_SEASON_VOTE_DICT = 'FAN_SEASON_VOTE_DICT'
    # _FAN_ARRAY = 'FAN_ARRAY'
    _IDOL_TOTAL_VOTE_DICT = 'IDOL_TOTAL_VOTE_DICT'
    _IDOL_SEASON_VOTE_DICT = 'IDOL_SEASON_VOTE_DICT'
    _IDOL_NAME_ARRAY = 'IDOL_NAME_ARRAY'
    _IDOL_DICT = 'IDOL_DICT'
    _IDOL_ARRAY = 'IDOL_ARRAY'
    _DAY_OF_SEASON_DICT = 'DAY_OF_SEASON_DICT'
    _DAY_LIMIT_VOTE_DICT = 'DAY_LIMIT_VOTE_DICT'
    _FAN_LIMIT_VOTE_DICT = 'FAN_LIMIT_VOTE_DICT'
    _DAY_LIMIT_CHARGE_DICT = 'DAY_LIMIT_CHARGE_DICT'
    
    _BARNER = 'BANNER'
    _CURRENT_SEASON_NAME = 'CURRENT_SEASON_NAME'
    _START_DATETIME = 'START_DATETIME'
    _END_DATETIME = 'END_DATETIME'

    _ONE_DAY_MILS = 86400
    _DAY_LIMIT_VOTE = 100
    _DAY_LIMIT_VOTE = 100

    _VOTE = 'vote'

    def __init__(self, db: IconScoreDatabase) -> None:
        super().__init__(db)
        # self._fan_dict = DictDB(_FAN_DICT, db, value_type=str)
        self._start_datetime = DictDB(self._START_DATETIME, db ,value_type=int)
        self._end_datetime = DictDB(self._END_DATETIME, db ,value_type=int)

        self._current_season_name = VarDB(self._CURRENT_SEASON_NAME, db ,value_type=str)
        self._day_of_season_dict = DictDB(self._DAY_OF_SEASON_DICT, db, value_type=str, depth=2)
        self._idol_total_vote_dict = DictDB(self._IDOL_TOTAL_VOTE_DICT, db, value_type=int, depth=2)
        self._idol_season_vote_dict = DictDB(self._IDOL_SEASON_VOTE_DICT, db, value_type=int, depth=3)
        self._fan_total_vote_dict = DictDB(self._FAN_TOTAL_VOTE_DICT, db, value_type=int, depth=3)
        self._fan_season_vote_dict = DictDB(self._FAN_SEASON_VOTE_DICT, db, value_type=int, depth=4)
        self._total_vote_dict = DictDB(self._FAN_SEASON_VOTE_DICT, db, value_type=int)
        self._total_season_vote_dict = DictDB(self._FAN_SEASON_VOTE_DICT, db, value_type=int, depth=2)
        # self._idol_name_array = ArrayDB(self._IDOL_NAME_ARRAY, db, value_type=str)
        self._idol_dict = DictDB(self._IDOL_DICT, db, value_type=str)
        self._idol_array = ArrayDB(self._IDOL_ARRAY, db, value_type=str)

        self._banner = VarDB(self._BARNER, db ,value_type=str)
        # self._fan_array = ArrayDB(self._FAN_ARRAY, db, value_type=str)

        self._day_limit_vote_dict = DictDB(self._DAY_LIMIT_VOTE_DICT, db, value_type=int, depth=2)
        self._fan_limit_vote_dict = DictDB(self._FAN_LIMIT_VOTE_DICT, db, value_type=int, depth=3)
        
        self._day_limit_charge_dict = DictDB(self._DAY_LIMIT_CHARGE_DICT, db, value_type=int)
        self._fan_limit_charge_dict = DictDB(self._DAY_LIMIT_CHARGE_DICT, db, value_type=bool, depth=2)

    def on_install(self) -> None:
        super().on_install()
     
    def on_update(self) -> None:
        super().on_update()

    @eventlog(indexed=2)
    def fallback_log(self, _from: Address, _amount: int):
        pass

    @payable
    def fallback(self):
        self.fallback_log(self.msg.sender, self.msg.value)

    def get_current_season_day(self)-> int:
        current_season_name = self._current_season_name.get()
        return int(((self.block.timestamp/1000000) - self._start_datetime[current_season_name]) / self._ONE_DAY_MILS)

    @eventlog
    def send_icx_log(self, _to: Address, _amount: int):
        pass

    # @external(readonly=True)
    # def get_balance(self) -> int:
    #     return self.icx.get_balance(self.address)
        
    @external
    def send_icx(self, _to: Address):
        if self.msg.sender != self.owner:
            revert('permission denied')

        day = self.get_current_season_day()

        if self._day_limit_charge_dict[day] >= 100:
            revert('일일 충전 제한량이 초과되었습니다.')
        if self._fan_limit_charge_dict[str(_to)][day] == True:
            revert('오늘은 이미 충전하였습니다.')

        amount = 1 * 10 ** 18

        if(self.icx.get_balance(self.address) < amount):
            revert('잔액이 부족하여 충전할 수 없습니다.')

        print(self.icx.get_balance(self.address))

        try:
            self.icx.transfer(_to, amount)
            self.send_icx_log(_to, amount)
            self._day_limit_charge_dict[day] += 1
            self._fan_limit_charge_dict[str(_to)][day] = True
        except:
            revert("충전에 실패하였습니다.")

    # @external
    # def set_banner(self, )

    @external
    def set_season_start_end_datetime(self, season_name: str, start_datetime: int, end_datetime: int):
        if self.msg.sender != self.owner:
            revert('permission denied')

        self._start_datetime[season_name] = start_datetime
        self._end_datetime[season_name] = end_datetime

    @external(readonly=True)
    def get_current_season_info(self) -> dict:
        season = {}
        season['season_name'] = self._current_season_name.get()
        season['start_datetime'] = self._start_datetime[season['season_name']]
        season['end_datetime'] = self._end_datetime[season['season_name']]
        return season

    @external
    def set_current_season_name(self, season_name: str):
        if self.msg.sender != self.owner:
            revert('permission denied')
            
        self._current_season_name.set(season_name)

    @external
    def add_idol(self, idol: str, image: str, message: str):
        if self.msg.sender != self.owner:
            revert('permission denied')

        if self._idol_dict[idol] != '':
            revert('idol already exists')

        json_data = {}
        json_data['idol'] = idol
        json_data['image'] = image
        json_data['message'] = message

        self._idol_dict[idol] = json_dumps(json_data)
        self._idol_array.put(json_dumps(json_data))

        self.add_idol_log(self._idol_dict[idol])
    
    @eventlog
    def add_idol_log(self, idol_json_data: str):
        pass
        
    @eventlog
    def update_idol_log(self, idol_json_data: str):
        pass

    @external
    def update_idol(self, idol: str, image: str, message: str):
        if self.msg.sender != self.owner:
            revert('permission denied')

        if self._idol_dict[idol] == '':
            revert('idol does not exists')

        json_data = {}
        json_data['idol'] = idol
        json_data['image'] = image
        json_data['message'] = message

        self._idol_dict[idol] = json_dumps(json_data)
        self.update_idol_log(self._idol_dict[idol])

    @external
    def vote(self, idol: str):
        if self._idol_dict[idol] == '':
            revert('idol does not exists')

        season_name = self._current_season_name.get()
        day = self.get_current_season_day()

        if self._day_limit_vote_dict[season_name][day] >= 20000:
            revert('전체 일일 투표 제한량 초과')
        
        if self._fan_limit_vote_dict[str(self.msg.sender)][season_name][day] >= 200:
            revert('개인 일일 투표 제한량 초과')

        self._total_vote_dict[self._VOTE] += 1
        self._idol_total_vote_dict[idol][self._VOTE] += 1
        self._total_season_vote_dict[season_name][self._VOTE] += 1
        self._idol_season_vote_dict[idol][season_name][self._VOTE] += 1
        self._fan_total_vote_dict[str(self.msg.sender)][idol][self._VOTE] += 1
        self._fan_season_vote_dict[str(self.msg.sender)][idol][season_name][self._VOTE] += 1

        self._day_limit_vote_dict[season_name][day] += 1 # 현재 시즌 경과일
        self._fan_limit_vote_dict[str(self.msg.sender)][season_name][day] += 1
        
        self.vote_log(self.msg.sender, idol)
    
    @eventlog
    def vote_log(self, sender: Address, idol: str):
        pass
  
    @external(readonly=True)
    def get_idol_list(self) -> dict:
        idol_temp_array = []
        for idol in self._idol_array:
            idol_temp_array.append(idol)
        return {'result': idol_temp_array}

    @external(readonly=True)
    def get_idol(self, idol: str) -> dict:
        return self._idol_dict[idol]

    @external(readonly=True)
    def get_idol_vote_count_by_season(self, idol: str, season_name: str) -> int:
        return self._idol_season_vote_dict[idol][season_name][self._VOTE]

    # @external(readonly=True)
    # def get_my_address(self) -> int:
    #     return str(self.msg.sender)

    @external(readonly=True)
    def get_block_timestamp(self) -> str:
        return str(self.block.timestamp)

    @external(readonly=True)
    def get_fan_vote_total_count(self, address:str, idol: str) -> int:
        return self._fan_total_vote_dict[address][idol][self._VOTE]

    @external(readonly=True)
    def get_fan_vote_season_count(self, address:str, season_name: str, idol: str) -> int:
        return self._fan_season_vote_dict[address][idol][season_name][self._VOTE]
    
    @external(readonly=True)
    def get_total_season_vote_count(self, season_name: str) -> int:
        return self._total_season_vote_dict[season_name][self._VOTE]
    
    @external(readonly=True)
    def get_total_vote_count(self) -> int:
        return self._total_vote_dict[self._VOTE]

    # @external(readonly=True)
    # def get_fan_list(self) -> dict:
    #     array_data = []
    #     for fan in self._fan_array:
    #         array_data.append(fan)

    #     return {'result': array_data}