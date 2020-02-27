===========================
HR (Extra) Hours Management
===========================

.. !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
   !! This file is generated by oca-gen-addon-readme !!
   !! changes will be overwritten.                   !!
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

.. |badge1| image:: https://img.shields.io/badge/maturity-Beta-yellow.png
    :target: https://odoo-community.org/page/development-status
    :alt: Beta
.. |badge2| image:: https://img.shields.io/badge/licence-AGPL--3-blue.png
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3
.. |badge3| image:: https://img.shields.io/badge/github-compassionCH%2Fcompassion--modules-lightgray.png?logo=github
    :target: https://github.com/compassionCH/compassion-modules/tree/11.0/hr_attendance_management
    :alt: compassionCH/compassion-modules

|badge1| |badge2| |badge3| 

This module extends the functionality of hr_attendance and allows to keep track of the
work hours of the employees, gives better overview of the work hours and follow the extra hours balance.

You can set in the schedule of the employee how much time they are supposed to work on a daily basis, allow
a maximum extra hours limit, and add minimum break time required. You will better keep track of the extra hours balance
of the employees given all the rules that you setup.

Furthermore, you can easily calculate the balance of an employee using the period system,
which calculates the balance between two dates. Actual balance is based on the balance of the last
period to avoid having to do many computations.

With this module, logging your hours is made easy in Odoo!

**Table of contents**

.. contents::
   :local:

Configuration
=============

To configure this module, go in **Attendances/Configuration/Attendance Settings**:

#. You can configure a *free break* time that is offered to employees. It means this time will count as a break time
   but won't be deduced from the attendance of the employees.
#. You can configure a *maximum extra hours limit*. When the employee makes more extra hours than the limit,
   it doesn't increase anymore his extra hours balance. This module offers to disable this continuous limit for some
   employee via the *continuous extra hours computation* flag in Employee. When unset, the limit will only be enforced
   once per year.
#. In **Attendances/Configuration/Break rules**  you can define a minimum break time required per day based on how many
   hours the employee worked on the day.
   Total break is the total break time the employee must do per day
   Minimum break is the minimum time required for at least one break (for instance if the employee should take at least
   30 minutes of break for lunch)
#. In **Attendances/Configuration/Coefficient** you can define special days that will give more extra hours to the
   employee. For instance you could set the Sunday to count 1.5x time. You can limit those rules to specific categories
   of employees.
#. In **Attendances/Manage Attendances/Employee** you can setup the *initial balance* of each employee,
   when you start using the module to count the hours.
   Just go in one employee, under the Hours tab, and set the value. The value will be updated each year to avoid
   computing over more than one year of attendances.
#. In **Attendances/Manage Attendances/Employee** you can setup a *continuous extra hours computation* for each employee.
   When unset, this allows the employee to get over the max_extra_hours limit. The max_extra_hours will however be enforced
   at the annual hours computation. The date of this computation can be set in *Attendance/Configuration/Next Balance Cron
   Execution*.
#. In **Employee/Contracts/Working Schedule** configure the working schedule of each employee by going to the
   *resource.calendar* object
#. In **Leaves/Configuration/Leave Types** configure if leave types should not deduce from the due hours of
   the employees by setting *Keep due hours*

To configure the cron which updates the balance of employees annually, go in **Settings/Technical/Automation/Automated Actions**:

#. In the cron *Compute annual extra hours balance* choose the scheduled date on which you want to apply the process to move the
   extra hours of employees in their annual balance and cap off the extra hours of employee with an annual extra hours
   computation. This is typically done at the beginning of the year. This process avoids the system to compute a huge amount of
   data after a few years of attendance.

Usage
=====

As an employee, you continue to log your attendance as before with the base module hr_attendance. But you have now
new views to keep track of your extra hours evolution.

#. In **Attendances/Manage Attendances/Attendance days** you can view all your working days with the hours that
   were registered.
#. In **Attendances/Manage Attendances/Balance history** you can view your extra hours evolution

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/116/10.0

Known issues / Roadmap
======================

* Improve leaves request to be able to specify how many hours it should deduct from the due hours

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/compassionCH/compassion-modules/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us smashing it by providing a detailed and welcomed
`feedback <https://github.com/compassionCH/compassion-modules/issues/new?body=module:%20hr_attendance_management%0Aversion:%2011.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.

Do not contact contributors directly about support or help with technical issues.

Credits
=======

Authors
~~~~~~~

* Compassion Switzerland

Contributors
~~~~~~~~~~~~

* Stéphane Eicher <eicher31@hotmail.com>
* Emanuel Cino <ecino@compassion.ch
* Nicolas Badoux <n.badoux@hotmail.com>
* Samuel Fringeli <samuel.fringeli@me.com>
* Quentin Gigon <gigon.quentin@gmail.com>

Other credits
~~~~~~~~~~~~~

Images
------

* Odoo Community Association: `Icon <https://odoo-community.org/logo.png>`_.

Maintainers
~~~~~~~~~~~

This module is maintained by Compassion Switzerland.

.. image:: https://upload.wikimedia.org/wikipedia/en/8/83/CompassionInternationalLogo.png
   :alt: Compassion Switzerland
   :target: https://www.compassion.ch

Compassion Switzerland is a nonprofit organization whose
mission is to release children from extreme poverty in Jesus name.

This module is part of the `compassionCH/compassion-modules <https://github.com/compassionCH/compassion-modules/tree/11.0/hr_attendance_management>`_ project on GitHub.

You are welcome to contribute.