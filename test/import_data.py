#coding=utf-8
__author__ = 'wanglu'

import time

from pyshop.models import *
from pyshop.helpers.sqla import *

if __name__ == "__main__":

    settings = {
        "sqlalchemy.url":"mysql+pymysql://root:root@localhost:3306/pyshop?charset=utf8mb4"
    }

    create_engine("pyshop",settings)
    session = SessionFactory.get("pyshop")()

    settings = {
        "sqlalchemy.url":"sqlite:///./main.db"
    }

    create_engine("pyshop",settings)
    sqlite_session = SessionFactory.get("pyshop")()
    #
    # users = sqlite_session.query(User).all()
    # for u in users:
    #     q = User.by_login(session,u.login,u.local)
    #     print q
    #     if User.by_login(session,u.login,u.local) is None:
    #         print u.id," ",u.login
    #         n_u = User()
    #         n_u.id = u.id
    #         n_u.login = u.login
    #         if u.password is not None:
    #             n_u.password = u.password
    #         n_u.firstname = u.firstname
    #         n_u.lastname = u.lastname
    #         n_u.email = u.email
    #         n_u.local = u.local
    #
    #         for group in u.groups:
    #             n_u.groups.append(Group.by_name(session,group.name))
    #
    #         session.add(n_u)
    #         session.flush()
    #
    # session.commit()


    # classifiers = sqlite_session.query(Classifier).all()
    #
    # for c in classifiers:
    #     n_c = Classifier()
    #     n_c.id = c.id
    #     n_c.name = c.name
    #     n_c.category = c.category
    #     #内部一对一关系
    #     if c.parent is not None:
    #         n_c.parent=Classifier.by_id(session,c.parent.id)
    #
    #     session.add(n_c)
    #     session.flush()
    #
    # session.commit()


    #导入包
    # pkgs = sqlite_session.query(Package).all()
    #
    # for pkg in pkgs:
    #     if Package.by_name(session,pkg.name) is None:
    #         n_pkg = Package()
    #         n_pkg.id = pkg.id
    #         n_pkg.name = pkg.name
    #         n_pkg.local = pkg.local
    #
    #         for owner in pkg.owners:
    #             n_pkg.owners.append(User.by_login(session,owner.login,owner.local))
    #         for maintainer in pkg.maintainers:
    #             n_pkg.maintainers.append(User.by_login(session,maintainer.login,maintainer.local))
    #
    #         for c in pkg.classifiers:
    #             n_pkg.classifiers.append(Classifier.by_id(session,c.id))
    #         session.add(n_pkg)
    #         session.flush()
    #
    # session.commit()

     #导入版本信息
    # rels = sqlite_session.query(Release).all()
    #
    # for rel in rels:
    #     n_rel = Release()
    #     n_rel.id = rel.id
    #     n_rel.version = rel.version
    #     if rel.summary:
    #         if len(rel.summary)>200:
    #             n_rel.summary = rel.summary[0:200]
    #         else:
    #             n_rel.summary = rel.summary
    #
    #     n_rel.downloads = rel.downloads
    #     n_rel.package_id = rel.package_id
    #     if User.by_id(session,rel.author_id) is None:
    #         if rel.author:
    #             user = User.by_login(session,rel.author.login,rel.author.local)
    #             if user:
    #                 n_rel.author_id = user.id
    #     else:
    #         n_rel.author_id = rel.author_id
    #     n_rel.maintainer_id = rel.maintainer_id
    #     n_rel.stable_version = rel.stable_version
    #     n_rel.home_page = rel.home_page
    #     n_rel.license = rel.license
    #     if rel.description:
    #         if len(rel.description)>1000:
    #             n_rel.description = rel.description[0:1000]
    #         else:
    #             n_rel.description = rel.description
    #     n_rel.keywords = rel.keywords
    #     n_rel.platform = rel.platform
    #     n_rel.download_url = rel.download_url
    #     n_rel.bugtrack_url = rel.bugtrack_url
    #     n_rel.docs_url = rel.docs_url
    #     for c in rel.classifiers:
    #         n_rel.classifiers.append(Classifier.by_id(session,c.id))
    #
    #     session.add(n_rel)
    #     session.flush()
    #
    # session.commit()

    # 导入版本的file
    rel_fs = sqlite_session.query(ReleaseFile).all()

    for r_f in rel_fs:
        n_r_f = ReleaseFile()
        n_r_f.id = r_f.id
        n_r_f.release_id = r_f.release_id
        n_r_f.filename = r_f.filename
        n_r_f.md5_digest = r_f.md5_digest
        n_r_f.size = r_f.size
        n_r_f.package_type = r_f.package_type
        n_r_f.python_version = r_f.python_version
        n_r_f.url = r_f.url
        n_r_f.downloads = r_f.downloads
        n_r_f.has_sig = r_f.has_sig
        n_r_f.comment_text = r_f.comment_text

        session.add(n_r_f)
        session.flush()
    session.commit()


