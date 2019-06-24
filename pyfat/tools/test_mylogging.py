#!/usr/bin/python
# -*- coding:utf-8 -*-


from pyfat.tools.mylogging import Logger


log = Logger('all.log', level='debug')
log.logger.debug('debug')
log.logger.info('info')
log.logger.warning('Warning')
log.logger.error('ReferenceError')
log.logger.critical('Severity')
Logger('error.log', level='error').logger.error('error')

