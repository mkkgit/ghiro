# Ghiro - Copyright (C) 2013-2016 Ghiro Developers.
# This file is part of Ghiro.
# See the file 'docs/LICENSE.txt' for license terms.

from django.db.models import Q

from hashes.models import List
from lib.analyzer.base import BaseProcessingModule

try:
    import hashlib
    IS_HASH = True
except ImportError:
    IS_HASH = False

class HashComparerProcessing(BaseProcessingModule):
    """Compares hashes with hashes lists."""

    name = "Hash List Comparer"
    description = "This plugins searches for a match between the image hash and hash lists."
    order = 20

    def check_deps(self):
        return IS_HASH

    def run(self, task):
        for key, value in self.data["hash"].iteritems():
            # Get all lists matching hash type.
            hash_lists = List.objects.filter(cipher=key).filter(Q(owner=task.owner) | Q(public=True))
            # Check hashes.
            for hash_list in hash_lists:
                if List.objects.filter(pk=hash_list.pk).filter(hash__value=value).exists():
                    hash_list.matches.add(task)

        return self.results
