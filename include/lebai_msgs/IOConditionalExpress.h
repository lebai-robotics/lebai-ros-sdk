// Generated by gencpp from file lebai_msgs/IOConditionalExpress.msg
// DO NOT EDIT!


#ifndef LEBAI_MSGS_MESSAGE_IOCONDITIONALEXPRESS_H
#define LEBAI_MSGS_MESSAGE_IOCONDITIONALEXPRESS_H


#include <string>
#include <vector>
#include <map>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>


namespace lebai_msgs
{
template <class ContainerAllocator>
struct IOConditionalExpress_
{
  typedef IOConditionalExpress_<ContainerAllocator> Type;

  IOConditionalExpress_()
    : group(0)
    , pin(0)
    , type(0)
    , float_value(0.0)
    , uint_value(0)
    , logic_operation(0)  {
    }
  IOConditionalExpress_(const ContainerAllocator& _alloc)
    : group(0)
    , pin(0)
    , type(0)
    , float_value(0.0)
    , uint_value(0)
    , logic_operation(0)  {
  (void)_alloc;
    }



   typedef uint32_t _group_type;
  _group_type group;

   typedef uint32_t _pin_type;
  _pin_type pin;

   typedef uint32_t _type_type;
  _type_type type;

   typedef double _float_value_type;
  _float_value_type float_value;

   typedef uint8_t _uint_value_type;
  _uint_value_type uint_value;

   typedef uint8_t _logic_operation_type;
  _logic_operation_type logic_operation;



// reducing the odds to have name collisions with Windows.h 
#if defined(_WIN32) && defined(GROUP_ROBOT)
  #undef GROUP_ROBOT
#endif
#if defined(_WIN32) && defined(GROUP_FLANGE)
  #undef GROUP_FLANGE
#endif
#if defined(_WIN32) && defined(TYPE_ANALOG)
  #undef TYPE_ANALOG
#endif
#if defined(_WIN32) && defined(TYPE_DIGITAL)
  #undef TYPE_DIGITAL
#endif
#if defined(_WIN32) && defined(LOGIC_OP_GT)
  #undef LOGIC_OP_GT
#endif
#if defined(_WIN32) && defined(LOGIC_OP_GE)
  #undef LOGIC_OP_GE
#endif
#if defined(_WIN32) && defined(LOGIC_OP_EQ)
  #undef LOGIC_OP_EQ
#endif
#if defined(_WIN32) && defined(LOGIC_OP_NE)
  #undef LOGIC_OP_NE
#endif
#if defined(_WIN32) && defined(LOGIC_OP_LT)
  #undef LOGIC_OP_LT
#endif
#if defined(_WIN32) && defined(LOGIC_OP_LE)
  #undef LOGIC_OP_LE
#endif

  enum {
    GROUP_ROBOT = 0u,
    GROUP_FLANGE = 1u,
    TYPE_ANALOG = 0u,
    TYPE_DIGITAL = 1u,
    LOGIC_OP_GT = 0u,
    LOGIC_OP_GE = 1u,
    LOGIC_OP_EQ = 2u,
    LOGIC_OP_NE = 3u,
    LOGIC_OP_LT = 4u,
    LOGIC_OP_LE = 5u,
  };


  typedef boost::shared_ptr< ::lebai_msgs::IOConditionalExpress_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::lebai_msgs::IOConditionalExpress_<ContainerAllocator> const> ConstPtr;

}; // struct IOConditionalExpress_

typedef ::lebai_msgs::IOConditionalExpress_<std::allocator<void> > IOConditionalExpress;

typedef boost::shared_ptr< ::lebai_msgs::IOConditionalExpress > IOConditionalExpressPtr;
typedef boost::shared_ptr< ::lebai_msgs::IOConditionalExpress const> IOConditionalExpressConstPtr;

// constants requiring out of line definition

   

   

   

   

   

   

   

   

   

   



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::lebai_msgs::IOConditionalExpress_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::lebai_msgs::IOConditionalExpress_<ContainerAllocator> >::stream(s, "", v);
return s;
}


template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator==(const ::lebai_msgs::IOConditionalExpress_<ContainerAllocator1> & lhs, const ::lebai_msgs::IOConditionalExpress_<ContainerAllocator2> & rhs)
{
  return lhs.group == rhs.group &&
    lhs.pin == rhs.pin &&
    lhs.type == rhs.type &&
    lhs.float_value == rhs.float_value &&
    lhs.uint_value == rhs.uint_value &&
    lhs.logic_operation == rhs.logic_operation;
}

template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator!=(const ::lebai_msgs::IOConditionalExpress_<ContainerAllocator1> & lhs, const ::lebai_msgs::IOConditionalExpress_<ContainerAllocator2> & rhs)
{
  return !(lhs == rhs);
}


} // namespace lebai_msgs

namespace ros
{
namespace message_traits
{





template <class ContainerAllocator>
struct IsFixedSize< ::lebai_msgs::IOConditionalExpress_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::lebai_msgs::IOConditionalExpress_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::lebai_msgs::IOConditionalExpress_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::lebai_msgs::IOConditionalExpress_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::lebai_msgs::IOConditionalExpress_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::lebai_msgs::IOConditionalExpress_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::lebai_msgs::IOConditionalExpress_<ContainerAllocator> >
{
  static const char* value()
  {
    return "35d2fc6b432f8da8c61c0faaba79afff";
  }

  static const char* value(const ::lebai_msgs::IOConditionalExpress_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0x35d2fc6b432f8da8ULL;
  static const uint64_t static_value2 = 0xc61c0faaba79afffULL;
};

template<class ContainerAllocator>
struct DataType< ::lebai_msgs::IOConditionalExpress_<ContainerAllocator> >
{
  static const char* value()
  {
    return "lebai_msgs/IOConditionalExpress";
  }

  static const char* value(const ::lebai_msgs::IOConditionalExpress_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::lebai_msgs::IOConditionalExpress_<ContainerAllocator> >
{
  static const char* value()
  {
    return "uint32 group\n"
"uint32 pin\n"
"uint32 type\n"
"float64 float_value\n"
"uint8 uint_value\n"
"uint8 logic_operation\n"
"\n"
"uint8 GROUP_ROBOT=0\n"
"uint8 GROUP_FLANGE=1\n"
"\n"
"uint8 TYPE_ANALOG=0\n"
"uint8 TYPE_DIGITAL=1\n"
"\n"
"# great >\n"
"uint8 LOGIC_OP_GT=0\n"
"# great and equal >=\n"
"uint8 LOGIC_OP_GE=1\n"
"# equal\n"
"uint8 LOGIC_OP_EQ=2\n"
"# not equal\n"
"uint8 LOGIC_OP_NE=3\n"
"# less than\n"
"uint8 LOGIC_OP_LT=4\n"
"# less than and equal\n"
"uint8 LOGIC_OP_LE=5\n"
"\n"
"\n"
"\n"
;
  }

  static const char* value(const ::lebai_msgs::IOConditionalExpress_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::lebai_msgs::IOConditionalExpress_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.group);
      stream.next(m.pin);
      stream.next(m.type);
      stream.next(m.float_value);
      stream.next(m.uint_value);
      stream.next(m.logic_operation);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct IOConditionalExpress_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::lebai_msgs::IOConditionalExpress_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::lebai_msgs::IOConditionalExpress_<ContainerAllocator>& v)
  {
    s << indent << "group: ";
    Printer<uint32_t>::stream(s, indent + "  ", v.group);
    s << indent << "pin: ";
    Printer<uint32_t>::stream(s, indent + "  ", v.pin);
    s << indent << "type: ";
    Printer<uint32_t>::stream(s, indent + "  ", v.type);
    s << indent << "float_value: ";
    Printer<double>::stream(s, indent + "  ", v.float_value);
    s << indent << "uint_value: ";
    Printer<uint8_t>::stream(s, indent + "  ", v.uint_value);
    s << indent << "logic_operation: ";
    Printer<uint8_t>::stream(s, indent + "  ", v.logic_operation);
  }
};

} // namespace message_operations
} // namespace ros

#endif // LEBAI_MSGS_MESSAGE_IOCONDITIONALEXPRESS_H