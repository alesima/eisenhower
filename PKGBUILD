# Maintainer: Alex Silva <contact@alesima.com>
pkgname=eisenhower-matrix
pkgver=1.1.1
pkgrel=1
pkgdesc="A GUI tool for task prioritization using the Eisenhower Matrix"
arch=('any')
url="https://github.com/alesima/eisenhower"
license=('MIT')
depends=(
    'python>=3.9'
    'python-gobject'
    'gtk4'
    'libadwaita'
)
makedepends=(
    'python-setuptools'
    'python-build'
    'python-installer'
    'python-wheel'
)
source=("$pkgname-$pkgver.tar.gz::$url/archive/v$pkgver.tar.gz")
sha256sums=('b42836f3e0be9def0c9177c7c83babcc6a70fb66e5f987209e874a5cfcd91305')

build() {
    cd "eisenhower-$pkgver"
    python -m build --wheel --no-isolation
}

package() {
    cd "eisenhower-$pkgver"
    python -m installer --destdir="$pkgdir" dist/*.whl

    # Install desktop file
    install -Dm644 io.github.alesima.eisenhower.desktop \
        "$pkgdir/usr/share/applications/io.github.alesima.eisenhower.desktop"

    # Install metainfo file
    install -Dm644 io.github.alesima.eisenhower.metainfo.xml \
        "$pkgdir/usr/share/metainfo/io.github.alesima.eisenhower.metainfo.xml"

    # Install icon
    install -Dm644 data/icons/io.github.alesima.eisenhower.svg \
        "$pkgdir/usr/share/icons/hicolor/scalable/apps/io.github.alesima.eisenhower.svg"

    # Install license
    install -Dm644 LICENSE "$pkgdir/usr/share/licenses/$pkgname/LICENSE"
}