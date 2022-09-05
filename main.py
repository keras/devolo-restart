#!/usr/bin/env python

import asyncio
import sys
import time
from typing import List
from devolo_plc_api import Device
from devolo_plc_api.network import async_discover_network

async def get_devices() -> List[Device]:
  devices = await async_discover_network()
  return list(devices.values())

async def restart_device(device: Device):
  print(f'[{device.ip}] Connect')
  await device.async_connect()
  print(f'[{device.ip}] Restart')
  assert(device.device)
  await device.device.async_restart()
  print(f'[{device.ip}] Disconnect')
  await device.async_disconnect()


async def main():
  devices = await get_devices()

  if not devices:
    print('No devices')
    sys.exit(1)

  for d in devices:
    await restart_device(d)
    time.sleep(10)

if __name__ == '__main__':
  asyncio.run(main())
