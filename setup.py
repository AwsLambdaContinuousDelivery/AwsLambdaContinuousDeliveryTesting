#!/usr/bin/env python

from distutils.core import setup

setup( name='pyAwsLambdaContinuousDeliveryTest'
     , version = '0.0.1'
     , description = 'pyAwsLambdaContinuousDeliveryTest'
     , author = 'Janos Potecki'
     , url = 'https://github.com/AwsLambdaContinuousDelivery/pyAwsLambdaContinuousDeliveryTest'
     , packages = ['awslambdacontinuousdelivery.python.test']
     , license='MIT'
     , install_requires = [ 
          'troposphere'
        , 'awacs'
        ]
     )
