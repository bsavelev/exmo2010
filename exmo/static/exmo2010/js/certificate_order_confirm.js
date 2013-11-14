// This file is part of EXMO2010 software.
// Copyright 2013 Foundation "Institute for Information Freedom Development"
// Copyright 2013 Al Nikolov
//
//    This program is free software: you can redistribute it and/or modify
//    it under the terms of the GNU Affero General Public License as
//    published by the Free Software Foundation, either version 3 of the
//    License, or (at your option) any later version.
//
//    This program is distributed in the hope that it will be useful,
//    but WITHOUT ANY WARRANTY; without even the implied warranty of
//    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//    GNU Affero General Public License for more details.
//
//    You should have received a copy of the GNU Affero General Public License
//    along with this program.  If not, see <http://www.gnu.org/licenses/>.
//
$(document).ready(function() {
    $('#previous_form').click(function(){
        var input = $("<input>").attr("type", "hidden").attr("name", "wizard_goto_step").val("0");
        $(this).closest('form').append($(input));
        $(this).closest('form').submit();
    });
});
