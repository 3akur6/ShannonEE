FROM pandare/pandadev:latest AS base

ENV TZ=Asia/Shanghai \
    LANG=en_US.UTF-8 \
    LANGUAGE=en_US:en \  
    LC_ALL=en_US.UTF-8
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone && \
    apt update && apt upgrade -y && \
    apt install -y locales gdb-multiarch && \
    sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && locale-gen

# Get ShannonEE framework
RUN git clone https://github.com/3akur6/ShannonEE /root/ShannonEE/

# Patch panda and rebuild
RUN mv /panda/ /root/panda/ && \
    patch -b /root/panda/target/arm/cpu.c /root/ShannonEE/panda.cpu.c.patch && \
    cd /root/panda/ && make distclean && rm -rf *-linux-user *-softmmu && \
    rm -r build/* && cd build && \
    ../build.sh arm-softmmu && \
    make install && \
    cd /root/panda/panda/python/core/ && python3 setup.py install

# Get avatar2, patch and build
RUN git clone https://github.com/avatartwo/avatar2 /root/avatar2/ && \
    cd /root/avatar2 && python3 setup.py install && \
    patch -b /usr/local/lib/python3.8/dist-packages/avatar2-1.4.6-py3.8.egg/avatar2/archs/arm.py /root/ShannonEE/avatar2.arm.py.patch

# Configure avatar2
RUN mkdir /root/.avatar2/ && cp /root/ShannonEE/avatar2.settings.cfg /root/.avatar2/settings.cfg
