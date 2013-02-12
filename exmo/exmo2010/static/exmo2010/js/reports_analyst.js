// This file is part of EXMO2010 software.
// Copyright 2010, 2011 Al Nikolov
// Copyright 2010, 2011, 2012 Institute for Information Freedom Development
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


$(document).ready(function() {
    var $headingClosed = $('td.report-title.closed'),
        $headingOpen = $('td.report-title.open'),
        $closed = $('.report-list-table.closed tbody'),
        $open = $('.report-list-table.open tbody'),
        url = $headingClosed.attr("rel");

    $closed.hide();

    $headingClosed.css('cursor','pointer');
    $headingOpen.css('cursor','pointer');

    $headingClosed.click(function() {
        if($closed.html() == "")
        {
            $closed.load(url, function(){
                var $count = $("table.report-list-table.closed td.count"),
                    count = parseInt($count.html()),
                    $title = $('td.report-title.closed'),
                    txt = $title.html();

                $title.html(txt+"("+count+")");
            });
        }
        $closed.toggle();
    });

    $headingOpen.click(function() {
        $open.toggle();
    });
});