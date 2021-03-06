// Generated by gencpp from file lebai_msgs/SetAOutMode.msg
// DO NOT EDIT!


#ifndef LEBAI_MSGS_MESSAGE_SETAOUTMODE_H
#define LEBAI_MSGS_MESSAGE_SETAOUTMODE_H

#include <ros/service_traits.h>


#include <lebai_msgs/SetAOutModeRequest.h>
#include <lebai_msgs/SetAOutModeResponse.h>


namespace lebai_msgs
{

struct SetAOutMode
{

typedef SetAOutModeRequest Request;
typedef SetAOutModeResponse Response;
Request request;
Response response;

typedef Request RequestType;
typedef Response ResponseType;

}; // struct SetAOutMode
} // namespace lebai_msgs


namespace ros
{
namespace service_traits
{


template<>
struct MD5Sum< ::lebai_msgs::SetAOutMode > {
  static const char* value()
  {
    return "faf7ab1e93a1650eb66028ad6d75331c";
  }

  static const char* value(const ::lebai_msgs::SetAOutMode&) { return value(); }
};

template<>
struct DataType< ::lebai_msgs::SetAOutMode > {
  static const char* value()
  {
    return "lebai_msgs/SetAOutMode";
  }

  static const char* value(const ::lebai_msgs::SetAOutMode&) { return value(); }
};


// service_traits::MD5Sum< ::lebai_msgs::SetAOutModeRequest> should match
// service_traits::MD5Sum< ::lebai_msgs::SetAOutMode >
template<>
struct MD5Sum< ::lebai_msgs::SetAOutModeRequest>
{
  static const char* value()
  {
    return MD5Sum< ::lebai_msgs::SetAOutMode >::value();
  }
  static const char* value(const ::lebai_msgs::SetAOutModeRequest&)
  {
    return value();
  }
};

// service_traits::DataType< ::lebai_msgs::SetAOutModeRequest> should match
// service_traits::DataType< ::lebai_msgs::SetAOutMode >
template<>
struct DataType< ::lebai_msgs::SetAOutModeRequest>
{
  static const char* value()
  {
    return DataType< ::lebai_msgs::SetAOutMode >::value();
  }
  static const char* value(const ::lebai_msgs::SetAOutModeRequest&)
  {
    return value();
  }
};

// service_traits::MD5Sum< ::lebai_msgs::SetAOutModeResponse> should match
// service_traits::MD5Sum< ::lebai_msgs::SetAOutMode >
template<>
struct MD5Sum< ::lebai_msgs::SetAOutModeResponse>
{
  static const char* value()
  {
    return MD5Sum< ::lebai_msgs::SetAOutMode >::value();
  }
  static const char* value(const ::lebai_msgs::SetAOutModeResponse&)
  {
    return value();
  }
};

// service_traits::DataType< ::lebai_msgs::SetAOutModeResponse> should match
// service_traits::DataType< ::lebai_msgs::SetAOutMode >
template<>
struct DataType< ::lebai_msgs::SetAOutModeResponse>
{
  static const char* value()
  {
    return DataType< ::lebai_msgs::SetAOutMode >::value();
  }
  static const char* value(const ::lebai_msgs::SetAOutModeResponse&)
  {
    return value();
  }
};

} // namespace service_traits
} // namespace ros

#endif // LEBAI_MSGS_MESSAGE_SETAOUTMODE_H
