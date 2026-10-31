cmake_minimum_required(VERSION 3.20)
project(sensorsimulation LANGUAGES CXX)
add_executable(sensorsimulation src/main.cpp)
target_compile_features(sensorsimulation PRIVATE cxx_std_17)
