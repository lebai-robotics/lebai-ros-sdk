// Generated by gencpp from file lebai_msgs/SetDOutRequest.msg
// DO NOT EDIT!


#ifndef LEBAI_MSGS_MESSAGE_SETDOUTREQUEST_H
#define LEBAI_MSGS_MESSAGE_SETDOUTREQUEST_H


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
struct SetDOutRequest_
{
  typedef SetDOutRequest_<ContainerAllocator> Type;

  SetDOutRequest_()
    : group(0)
    , index(0)
    , value(false)  {
    }
  SetDOutRequest_(const ContainerAllocator& _alloc)
    : group(0)
    , index(0)
    , value(false)  {
  (void)_alloc;
    }



   typedef uint8_t _group_type;
  _group_type group;

   typedef uint16_t _index_type;
  _index_type index;

   typedef uint8_t _value_type;
  _value_type value;





  typedef boost::shared_ptr< ::lebai_msgs::SetDOutRequest_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::lebai_msgs::SetDOutRequest_<ContainerAllocator> const> ConstPtr;

}; // struct SetDOutRequest_

typedef ::lebai_msgs::SetDOutRequest_<std::allocator<void> > SetDOutRequest;

typedef boost::shared_ptr< ::lebai_msgs::SetDOutRequest > SetDOutRequestPtr;
typedef boost::shared_ptr< ::lebai_msgs::SetDOutRequest const> SetDOutRequestConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::lebai_msgs::SetDOutRequest_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::lebai_msgs::SetDOutRequest_<ContainerAllocator> >::stream(s, "", v);
return s;
}


template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator==(const ::lebai_msgs::SetDOutRequest_<ContainerAllocator1> & lhs, const ::lebai_msgs::SetDOutRequest_<ContainerAllocator2> & rhs)
{
  return lhs.group == rhs.group &&
    lhs.index == rhs.index &&
    lhs.value == rhs.value;
}

template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator!=(const ::lebai_msgs::SetDOutRequest_<ContainerAllocator1> & lhs, const ::lebai_msgs::SetDOutRequest_<ContainerAllocator2> & rhs)
{
  return !(lhs == rhs);
}


} // namespace lebai_msgs

namespace ros
{
namespace message_traits
{





template <class ContainerAllocator>
struct IsFixedSize< ::lebai_msgs::SetDOutRequest_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::lebai_msgs::SetDOutRequest_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::lebai_msgs::SetDOutRequest_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::lebai_msgs::SetDOutRequest_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::lebai_msgs::SetDOutRequest_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::lebai_msgs::SetDOutRequest_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::lebai_msgs::SetDOutRequest_<ContainerAllocator> >
{
  static const char* value()
  {
    return "9e6bfbd7584e5f4dc49295cc14286131";
  }

  static const char* value(const ::lebai_msgs::SetDOutRequest_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0x9e6bfbd7584e5f4dULL;
  static const uint64_t static_value2 = 0xc49295cc14286131ULL;
};

template<class ContainerAllocator>
struct DataType< ::lebai_msgs::SetDOutRequest_<ContainerAllocator> >
{
  static const char* value()
  {
    return "lebai_msgs/SetDOutRequest";
  }

  static const char* value(const ::lebai_msgs::SetDOutRequest_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::lebai_msgs::SetDOutRequest_<ContainerAllocator> >
{
  static const char* value()
  {
    return "uint8 group\n"
"uint16 index\n"
"bool value\n"
;
  }

  static const char* value(const ::lebai_msgs::SetDOutRequest_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::lebai_msgs::SetDOutRequest_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.group);
      stream.next(m.index);
      stream.next(m.value);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct SetDOutRequest_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::lebai_msgs::SetDOutRequest_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::lebai_msgs::SetDOutRequest_<ContainerAllocator>& v)
  {
    s << indent << "group: ";
    Printer<uint8_t>::stream(s, indent + "  ", v.group);
    s << indent << "index: ";
    Printer<uint16_t>::stream(s, indent + "  ", v.index);
    s << indent << "value: ";
    Printer<uint8_t>::stream(s, indent + "  ", v.value);
  }
};

} // namespace message_operations
} // namespace ros

#endif // LEBAI_MSGS_MESSAGE_SETDOUTREQUEST_H