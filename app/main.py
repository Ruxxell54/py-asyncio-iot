import asyncio
import time
from typing import Awaitable, Any

from iot.devices import HueLightDevice, SmartSpeakerDevice, SmartToiletDevice
from iot.message import Message, MessageType
from iot.service import IOTService


async def run_sequence(*functions: Awaitable[Any]) -> None:
    for function in functions:
        await function


async def run_parallel(*functions: Awaitable[Any]) -> tuple[Any]:
    return await asyncio.gather(*functions)


async def main() -> None:
    # create an IOT service
    service = IOTService()

    # create and register a few devices
    hue_light = HueLightDevice()
    speaker = SmartSpeakerDevice()
    toilet = SmartToiletDevice()
    results = await run_parallel(
        service.register_device(hue_light),
        service.register_device(speaker),
        service.register_device(toilet)
    )

    hue_light_id, speaker_id, toilet_id = results[0], results[1], results[2]
    # create a few programs
    await run_sequence(
        service.run_program([
            Message(hue_light_id, MessageType.SWITCH_ON),
            Message(speaker_id, MessageType.SWITCH_ON),
            Message(speaker_id, MessageType.PLAY_SONG, "Rick Astley - Never Gonna Give You Up")]
        )
    )

    await run_sequence(
        service.run_program(
            [Message(hue_light_id, MessageType.SWITCH_OFF),
             Message(speaker_id, MessageType.SWITCH_OFF),
             Message(toilet_id, MessageType.FLUSH),
             Message(toilet_id, MessageType.CLEAN), ]
        )
    )


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    end = time.perf_counter()

    print("Elapsed:", end - start)
