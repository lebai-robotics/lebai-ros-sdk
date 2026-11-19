#!/usr/bin/env python3

import argparse

import rospy
from lebai_interfaces.srv import SetAnalogOutput, SetDigitalOutput

from lebai_tutorials_common import checked_response


def main():
    parser = argparse.ArgumentParser(description='Set a digital or analog output.')
    parser.add_argument('--device', default='robot')
    parser.add_argument('--pin', type=int, required=True, help='output pin index')
    output = parser.add_mutually_exclusive_group(required=True)
    output.add_argument('--digital', type=int, choices=(0, 1))
    output.add_argument('--analog', type=float, help='analog output value')
    args = parser.parse_args(rospy.myargv()[1:])
    if args.pin < 0:
        parser.error('--pin must be nonnegative')

    rospy.init_node('io_example')
    if args.digital is not None:
        name, service, value = '/lebai/io/set_do', SetDigitalOutput, bool(args.digital)
    else:
        name, service, value = '/lebai/io/set_ao', SetAnalogOutput, args.analog

    try:
        rospy.wait_for_service(name, timeout=5.0)
        proxy = rospy.ServiceProxy(name, service)
        checked_response(name, proxy(device=args.device, pin=args.pin, value=value))
    except (rospy.ROSException, rospy.ServiceException, RuntimeError) as exc:
        rospy.logerr('%s', exc)
        return 1
    rospy.loginfo('Set %s pin %s to %s', args.device, args.pin, value)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
