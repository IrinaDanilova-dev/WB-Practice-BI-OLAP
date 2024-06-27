CREATE ROLE  readonly_role ;

GRANT SELECT ON *.* TO readonly_role;

create user readonly_user_1 identified with sha256_password by 'ru_pwd1' ;

grant readonly_role to readonly_user_1 ;

CREATE ROLE  stage_role ;

GRANT create , insert ON stage.* TO stage_role;

create user stage_user_1 identified with sha256_password by 'stu_pwd1' ;

grant stage_role to stage_user_1 ;
