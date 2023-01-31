# flake8: noqa
import typing

if typing.TYPE_CHECKING:
    from dataclasses import dataclass
else:
    from memorix_client_redis import dataclass

from enum import Enum
from memorix_client_redis import (
    MemorixClientApi,
    MemorixClientApiDefaults as _MemorixClientApiDefaults,
    MemorixClientCacheApi,
    MemorixClientCacheApiItem,
    MemorixClientCacheApiItemNoKey,
    MemorixClientCacheSetOptions as _MemorixClientCacheSetOptions,
    MemorixClientCacheSetOptionsExpire as _MemorixClientCacheSetOptionsExpire,
    MemorixClientPubSubApi,
    MemorixClientPubSubApiItem,
    MemorixClientPubSubApiItemNoKey,
    MemorixClientTaskApi,
    MemorixClientTaskApiItem,
    MemorixClientTaskApiItemNoKey,
    MemorixClientTaskApiItemNoReturns,
    MemorixClientTaskApiItemNoKeyNoReturns,
    MemorixClientTaskDequequeOptions as _MemorixClientTaskDequequeOptions,
)


MemorixClientApiDefaults = _MemorixClientApiDefaults
MemorixClientCacheSetOptions = _MemorixClientCacheSetOptions
MemorixClientCacheSetOptionsExpire = _MemorixClientCacheSetOptionsExpire
MemorixClientTaskDequequeOptions = _MemorixClientTaskDequequeOptions


class DetectionType(str, Enum):
    MAVIC = "MAVIC"
    PHANTOM = "PHANTOM"
    EVO = "EVO"
    WIFI = "WIFI"


class SaveRecord(str, Enum):
    OFF = "OFF"
    ALL = "ALL"
    DETECTIONS = "DETECTIONS"
    NO_DETECTIONS = "NO_DETECTIONS"


class Status(str, Enum):
    IDLE = "IDLE"
    RUNNING = "RUNNING"


@dataclass
class CacheLocalization_keyKey(object):
    access_token: "str"
    iteration_num: int


@dataclass
class CacheRecord_dataPayload(object):
    iteration_num: int
    curr_detection_range: "DetectionRange"


@dataclass
class CacheDetection_dataPayload(object):
    identifier: str
    save_record: "SaveRecord"


@dataclass
class CacheLocalization_iteration_dataPayload(object):
    freq_offset: float


@dataclass
class PubSubDetectionsPayload(object):
    detection_type: typing.Optional["DetectionType"]
    detection_range: "DetectionRange"
    num_of_good_gap: int
    min_wanted_gap: int
    iteration_num: int
    all_max_corrs: typing.List[float]
    all_len_peaks: typing.List[int]
    all_gaps: typing.List[int]


@dataclass
class PubSubStart_detectionPayload(object):
    default_detection_ranges: typing.List["DetectionRange"]
    save_record: "SaveRecord"


@dataclass
class DetectionRange(object):
    f_start_mhz: float
    f_end_mhz: float
    rate_mhz_s: float
    duration_s: float


@dataclass
class DetectionRangeData(object):
    gaps: int
    visits: int


class MemorixCacheApi(MemorixClientCacheApi):
    def __init__(self, api: MemorixClientApi) -> None:
        super().__init__(api=api)

        self.status = MemorixClientCacheApiItemNoKey["Status"](
            api=self._api,
            id="status",
            payload_class=Status,
        )
        self.is_new_range = MemorixClientCacheApiItemNoKey["bool"](
            api=self._api,
            id="is_new_range",
            payload_class=bool,
        )
        self.should_stop_detection = MemorixClientCacheApiItemNoKey["bool"](
            api=self._api,
            id="should_stop_detection",
            payload_class=bool,
        )
        self.detection_ranges = MemorixClientCacheApiItemNoKey[
            typing.List["DetectionRange"]
        ](
            api=self._api,
            id="detection_ranges",
            payload_class=typing.List[DetectionRange],
        )
        self.detection_range_data = MemorixClientCacheApiItem[
            "DetectionRange", "DetectionRangeData"
        ](
            api=self._api,
            id="detection_range_data",
            payload_class=DetectionRangeData,
        )
        self.record_data = MemorixClientCacheApiItem[str, "CacheRecord_dataPayload"](
            api=self._api,
            id="record_data",
            payload_class=CacheRecord_dataPayload,
        )
        self.detection_data = MemorixClientCacheApiItemNoKey[
            "CacheDetection_dataPayload"
        ](
            api=self._api,
            id="detection_data",
            payload_class=CacheDetection_dataPayload,
        )
        self.localization_key = MemorixClientCacheApiItem[
            "CacheLocalization_keyKey", str
        ](
            api=self._api,
            id="localization_key",
            payload_class=str,
        )
        self.localization_iteration_data = MemorixClientCacheApiItem[
            str, "CacheLocalization_iteration_dataPayload"
        ](
            api=self._api,
            id="localization_iteration_data",
            payload_class=CacheLocalization_iteration_dataPayload,
        )


class MemorixPubSubApi(MemorixClientPubSubApi):
    def __init__(self, api: MemorixClientApi) -> None:
        super().__init__(api=api)

        self.record = MemorixClientPubSubApiItemNoKey[str](
            api=self._api,
            id="record",
            payload_class=str,
        )
        self.detections = MemorixClientPubSubApiItemNoKey["PubSubDetectionsPayload"](
            api=self._api,
            id="detections",
            payload_class=PubSubDetectionsPayload,
        )
        self.start_detection = MemorixClientPubSubApiItemNoKey[
            "PubSubStart_detectionPayload"
        ](
            api=self._api,
            id="start_detection",
            payload_class=PubSubStart_detectionPayload,
        )
        self.status_changed = MemorixClientPubSubApiItemNoKey[bool](
            api=self._api,
            id="status_changed",
            payload_class=bool,
        )


class MemorixTaskApi(MemorixClientTaskApi):
    def __init__(self, api: MemorixClientApi) -> None:
        super().__init__(api=api)

        self.detect = MemorixClientTaskApiItemNoKeyNoReturns[str](
            api=self._api,
            id="detect",
            payload_class=str,
        )


class MemorixApi(MemorixClientApi):
    def __init__(
        self,
        redis_url: str,
        defaults: typing.Optional[MemorixClientApiDefaults] = None,
    ) -> None:
        super().__init__(redis_url=redis_url, defaults=defaults)

        self.cache = MemorixCacheApi(self)
        self.pubsub = MemorixPubSubApi(self)
        self.task = MemorixTaskApi(self)