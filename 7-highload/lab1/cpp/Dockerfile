FROM devenv

RUN mkdir /project
WORKDIR /project

COPY conanfile.txt ./
RUN mkdir build && cd build && conan install .. 

COPY main.cpp CMakeLists.txt ./

WORKDIR /project/build
RUN cmake .. -DCMAKE_BUILD_TYPE=Release
RUN cmake --build .


WORKDIR /project/build/bin
CMD [ "./main" ]
