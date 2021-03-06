// Generated by gencpp from file lebai_msgs/MoveCircle.msg
// DO NOT EDIT!


#ifndef LEBAI_MSGS_MESSAGE_MOVECIRCLE_H
#define LEBAI_MSGS_MESSAGE_MOVECIRCLE_H

#include <ros/service_traits.h>


#include <lebai_msgs/MoveCircleRequest.h>
#include <lebai_msgs/MoveCircleResponse.h>


namespace lebai_msgs
{

struct MoveCircle
{

typedef MoveCircleRequest Request;
typedef MoveCircleResponse Response;
Request request;
Response response;

typedef Request RequestType;
typedef Response ResponseType;

}; // struct MoveCircle
} // namespace lebai_msgs


namespace ros
{
namespace service_traits
{


template<>
struct MD5Sum< ::lebai_msgs::MoveCircle > {
  static const char* value()
  {
    return "76aefbda84057bd81221aca855230727";
  }

  static const char* value(const ::lebai_msgs::MoveCircle&) { return value(); }
};

template<>
struct DataType< ::lebai_msgs::MoveCircle > {
  static const char* value()
  {
    return "lebai_msgs/MoveCircle";
  }

  static const char* value(const ::lebai_msgs::MoveCircle&) { return value(); }
};


// service_traits::MD5Sum< ::lebai_msgs::MoveCircleRequest> should match
// service_traits::MD5Sum< ::lebai_msgs::MoveCircle >
template<>
struct MD5Sum< ::lebai_msgs::MoveCircleRequest>
{
  static const char* value()
  {
    return MD5Sum< ::lebai_msgs::MoveCircle >::value();
  }
  static const char* value(const ::lebai_msgs::MoveCircleRequest&)
  {
    return value();
  }
};

// service_traits::DataType< ::lebai_msgs::MoveCircleRequest> should match
// service_traits::DataType< ::lebai_msgs::MoveCircle >
template<>
struct DataType< ::lebai_msgs::MoveCircleRequest>
{
  static const char* value()
  {
    return DataType< ::lebai_msgs::MoveCircle >::value();
  }
  static const char* value(const ::lebai_msgs::MoveCircleRequest&)
  {
    return value();
  }
};

// service_traits::MD5Sum< ::lebai_msgs::MoveCircleResponse> should match
// service_traits::MD5Sum< ::lebai_msgs::MoveCircle >
template<>
struct MD5Sum< ::lebai_msgs::MoveCircleResponse>
{
  static const char* value()
  {
    return MD5Sum< ::lebai_msgs::MoveCircle >::value();
  }
  static const char* value(const ::lebai_msgs::MoveCircleResponse&)
  {
    return value();
  }
};

// service_traits::DataType< ::lebai_msgs::MoveCircleResponse> should match
// service_traits::DataType< ::lebai_msgs::MoveCircle >
template<>
struct DataType< ::lebai_msgs::MoveCircleResponse>
{
  static const char* value()
  {
    return DataType< ::lebai_msgs::MoveCircle >::value();
  }
  static const char* value(const ::lebai_msgs::MoveCircleResponse&)
  {
    return value();
  }
};

} // namespace service_traits
} // namespace ros

#endif // LEBAI_MSGS_MESSAGE_MOVECIRCLE_H
