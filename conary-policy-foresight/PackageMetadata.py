#
# Copyright (c) 2008 The Foresight Linux Project
#
# This program is distributed under the terms of the Common Public License,
# version 1.0. A copy of this license should have been distributed with this
# source file in a file called LICENSE. If it is not present, the license
# is always available at http://www.rpath.com/permanent/licenses/CPL-1.0.
#
# This program is distributed in the hope that it will be useful, but
# without any warranty; without even the implied warranty of merchantability
# or fitness for a particular purpose. See the Common Public License for
# full details.
#


from conary.build import policy

class SetPackageMetadataFromRecipe(policy.DestdirPolicy):
    # Cannot be a PackagePolicy because that is a subsequent
    # bucket that runs after Requires
    requires = (
        ('Requires', policy.REQUIRED_SUBSEQUENT),
    )
    processUnmodified = False

    def do(self):
        if  hasattr(self.recipe, 'packageSummary'):
            if not hasattr(self.recipe, 'packageDescription'):
                self.recipe.packageDescription =  ''
                self.info('Package description incomplete; packageSummary defined but not packageDescription... please consider fixing it')
            self.recipe.Description(shortDesc =  self.recipe.packageSummary, longDesc =  self.recipe.packageDescription, macros = True)
        else:
            self.info('Package descriptions are not set; Application metadata is critical for a good user experience. Please consider fixing it')
